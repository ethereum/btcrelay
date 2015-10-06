from ethereum import tester

import datetime
import struct
import pytest
slow = pytest.mark.slow

from utilRelay import getHeaderBytes, dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestBtcRelay(object):
    CONTRACT_DEBUG = 'test/btcrelay_debug.se'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(2.35e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    # fork from 6 blocks ago, using blocks with same difficulty
    def testForkingPast(self):
        block10Prev = 0x000000008d9dc510f23c2657fc4f67bea30078cc05a90eb89e84cc475c080805
        self.c.setInitialParent(block10Prev, 9, 1)

        headers = [
            '010000000508085c47cc849eb80ea905cc7800a3be674ffc57263cf210c59d8d00000000112ba175a1e04b14ba9e7ea5f76ab640affeef5ec98173ac9799a852fa39add320cd6649ffff001d1e2de565',
            '01000000e915d9a478e3adf3186c07c61a22228b10fd87df343c92782ecc052c000000006e06373c80de397406dc3d19c90d71d230058d28293614ea58d6a57f8f5d32f8b8ce6649ffff001d173807f8',
            '010000007330d7adf261c69891e6ab08367d957e74d4044bc5d9cd06d656be9700000000b8c8754fabb0ffeb04ca263a1368c39c059ca0d4af3151b876f27e197ebb963bc8d06649ffff001d3f596a0c',
            '010000005e2b8043bd9f8db558c284e00ea24f78879736f4acd110258e48c2270000000071b22998921efddf90c75ac3151cacee8f8084d3e9cb64332427ec04c7d562994cd16649ffff001d37d1ae86',
            '0100000089304d4ba5542a22fb616d1ca019e94222ee45c1ad95a83120de515c00000000560164b8bad7675061aa0f43ced718884bdd8528cae07f24c58bb69592d8afe185d36649ffff001d29cbad24',
            '01000000378a6f6593e2f0251132d96616e837eb6999bca963f6675a0c7af180000000000d080260d107d269ccba9247cfc64c952f1d13514b49e9f1230b3a197a8b7450fa276849ffff001d38d8fb98',
            '010000007384231257343f2fa3c55ee69ea9e676a709a06dcfd2f73e8c2c32b300000000442ee91b2b999fb15d61f6a88ecf2988e9c8ed48f002476128e670d3dac19fe706286849ffff001d049e12d6'
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])
            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+10

        cumulDiff = self.c.getCumulativeDifficulty()

        # block hashes
        b0 = 0x000000002c05cc2e78923c34df87fd108b22221ac6076c18f3ade378a4d915e9
        b1 = 0x0000000097be56d606cdd9c54b04d4747e957d3608abe69198c661f2add73073 # block #100001
        b2 = 0x0000000027c2488e2510d1acf4369787784fa20ee084c258b58d9fbd43802b5e
        b3 = 0x000000005c51de2031a895adc145ee2242e919a01c6d61fb222a54a54b4d3089
        b4 = 0x0000000080f17a0c5a67f663a9bc9969eb37e81666d9321125f0e293656f8a37
        b5 = 0x00000000b3322c8c3ef7d2cf6da009a776e6a99ee65ec5a32f3f345712238473
        b6 = 0x00000000174a25bb399b009cc8deff1c4b3ea84df7e93affaaf60dc3416cc4f5

        # values are from block 10
        tx = 0xd3ad39fa52a89997ac7381c95eeffeaf40b66af7a57e9eba144be0a175a12b11
        txIndex = 0
        sibling = []


        txBlockHash = 0xdead
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0

        # b1 is within6confirms so should NOT verify
        txBlockHash = b1
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0


        # verifyTx should only return 1 for b0
        txBlockHash = b0
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 1

        assert b6 == self.c.getBlockchainHead()


        # insert blocks to create a fork from the start (block 9)
        # using script/mine.py these are the next 7 blocks
        # nonce: 0 blockhash: fill txBlockHash first
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        # nonce: 0 blockhash: 02c67135bd91986f9aaf3f0818baab439202fe5c34400c2c10bff6cd1336d436
        # nonce: 1 blockhash: 6e60065cc981914c23897143c75f0cde6e456df65f23afd41ddc6e6ce86b2b63
        # nonce: 1 blockhash: 38a052cdf4ef0fddf2de88e687163db7f39cb8de738fa9f5e871a72fc74c57c1
        # nonce: 0 blockhash: 2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c

        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xd3ad39fa52a89997ac7381c95eeffeaf40b66af7a57e9eba144be0a175a12b11
        time = 1231473952  # from block10
        bits = 0x1d00ffff  # from block10
        nonce = 1
        hashPrevBlock = block10Prev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(blockHeaderBytes)
            hashPrevBlock = dblSha256Flip(blockHeaderBytes)

            # print('@@@@ fake chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+10  # fake blocks are stored since there is possibility they can become the main chain

        assert self.c.getCumulativeDifficulty() == cumulDiff  # cumulDiff should not change
        assert b6 == self.c.getBlockchainHead()

        # forked block should NOT verify
        txBlockHash = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0

        # b0 should still verify
        txBlockHash = b0
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 1


    # TODO
    def testHeadersFrom100K(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])
            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000

        cumulDiff = self.c.getCumulativeDifficulty()

        # block hashes
        b0 = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        b1 = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090 # block #100001
        b2 = 0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
        b3 = 0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1
        b4 = 0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79
        b5 = 0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45
        b6 = 0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60

        # values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49


        txBlockHash = 0xdead
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0

        # b1 is within6confirms so should NOT verify
        txBlockHash = b1
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0


        # verifyTx should only return 1 for b0
        txBlockHash = b0
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 1

        assert b6 == self.c.getBlockchainHead()


        # insert (fake) blocks that will not be on main chain
        # using script/mine.py (commit 3908709) these are the next 7 blocks
        # nonce: 0 blockhash: 11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        # nonce: 0 blockhash: 02c67135bd91986f9aaf3f0818baab439202fe5c34400c2c10bff6cd1336d436
        # nonce: 1 blockhash: 6e60065cc981914c23897143c75f0cde6e456df65f23afd41ddc6e6ce86b2b63
        # nonce: 1 blockhash: 38a052cdf4ef0fddf2de88e687163db7f39cb8de738fa9f5e871a72fc74c57c1
        # nonce: 0 blockhash: 2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c

        # https://bitcoin.org/en/developer-reference#target-nbits
        # Difficulty 1, the minimum allowed difficulty, is represented on
        # mainnet and the current testnet by the nBits value 0x1d00ffff.
        # Regtest mode uses a different difficulty 1 value of 0x207fffff,
        # the highest possible value below uint32_max which can be encoded;
        # this allows near-instant building of blocks in regtest mode.
        REGTEST_EASIEST_DIFFICULTY = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = REGTEST_EASIEST_DIFFICULTY
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(blockHeaderBytes)
            hashPrevBlock = dblSha256Flip(blockHeaderBytes)

            # print('@@@@ fake chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000  # fake blocks are stored since there is possibility they can become the main chain

        assert self.c.getCumulativeDifficulty() == cumulDiff  # cumulDiff should not change
        assert b6 == self.c.getBlockchainHead()

        # forked block should NOT verify
        txBlockHash = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0

        # b0 should still verify
        txBlockHash = b0
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 1


    # test that a tx that verifies, does not verify after a reorg causes it to
    # no longer be on the main chain
    def testReorg(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)



        # tx for verification: values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49




        # insert (easy) blocks
        # using script/mine.py these are the next 7 blocks
        # nonce: 0 blockhash: 11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        # nonce: 0 blockhash: 02c67135bd91986f9aaf3f0818baab439202fe5c34400c2c10bff6cd1336d436
        # nonce: 1 blockhash: 6e60065cc981914c23897143c75f0cde6e456df65f23afd41ddc6e6ce86b2b63
        # nonce: 1 blockhash: 38a052cdf4ef0fddf2de88e687163db7f39cb8de738fa9f5e871a72fc74c57c1
        # nonce: 0 blockhash: 2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c
        REGTEST_EASIEST_DIFFICULTY = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = REGTEST_EASIEST_DIFFICULTY
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(blockHeaderBytes)
            hashPrevBlock = dblSha256Flip(blockHeaderBytes)
            assert res == i+100000

        # testingonlySetHeaviest is needed because the difficulty from
        # REGTEST_EASIEST_DIFFICULTY becomes 0 and so the score does not
        # increase, meaning that heaviesBlock also does not change
        self.c.testingonlySetHeaviest(0x2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c)

        firstEasyBlock = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, txIndex, sibling, firstEasyBlock)
        assert res == 1


        # reorg: add headers with more PoW (difficulty)
        # add headers one by one and tx should only be verified when the
        # last header is added, ie tx has enough confirmations
        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        block100k = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])
            assert res == i+100000

            # firstEasyBlock should no longer verify since it is no longer on the main chain
            res = self.c.verifyTx(tx, txIndex, sibling, firstEasyBlock)
            assert res == 0

            # block100k should only verify when it has enough confirmations
            res = self.c.verifyTx(tx, txIndex, sibling, block100k)
            exp = 1 if i==6 else 0
            assert res == exp



    def testWithin6Confirms(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])
            assert res == i+100000


        blockHash = [
            0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506,
            0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090, # block #100001
            0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af,
            0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1,
            0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79,
            0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45,
            0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60
        ]

        for i, bh in enumerate(blockHash):
            res = self.c.within6Confirms(bh, profiling=True)
            print('GAS: '+str(res['gas']))
            exp = 0 if i==0 else 1
            assert res['output'] == exp


    def storeGenesisBlock(self):
        self.c.setInitialParent(0, 0, 1)

        blockHeaderStr = ("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBytes, profiling=True)
        return res

    def storeBlock1(self):
        # block 1
        blockHeaderStr = ("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299")
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBytes, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == 2  # genesis block is at height 1


    def testStoringHeaders(self):
        res = self.storeGenesisBlock()
        print('GAS: '+str(res['gas']))
        assert res['output'] == 1

        self.storeBlock1()

        block1Hash = 0x00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048
        assert self.c.getBlockchainHead() == block1Hash
        assert self.c.getLastBlockHeight() == 1 + 1  # +1 since setInitialParent was called with imaginary block

        assert self.c.getCumulativeDifficulty() == 2 + 1  # +1 since setInitialParent was called with imaginary block


    def testStoreNewHead(self):
        parent = 0x00000000000000000a15bda775b0004fca6368c5b8a61cb0d3b793670b9369c2
        height = 357368
        cumulDifficulty = 1981747039106115  # 1981795846593359 - 48807487244 (diff at 357369)
        self.c.setInitialParent(parent, height, cumulDifficulty)

        orphanStr = '03000000c269930b6793b7d3b01ca6b8c56863ca4f00b075a7bd150a0000000000000000391c579bd59cb0199baf96dc1bc1066de0dc202bbe18f062a20aa25f78729376ba6f5d55f586161826f45178'
        bhBytes = orphanStr.decode('hex')

        orphanHash = 0x00000000000000000db6ab0aa23c28fc707f05f1646d25dba684ffe316bcf24d
        assert dblSha256Flip(bhBytes) == orphanHash

        assert self.c.storeBlockHeader(bhBytes) == height + 1
        assert self.c.getBlockchainHead() == orphanHash
        assert self.c.getLastBlockHeight() == height + 1
        assert self.c.getCumulativeDifficulty() == 1981795846593359

        # real 357369
        headerStr = '03000000c269930b6793b7d3b01ca6b8c56863ca4f00b075a7bd150a00000000000000004bdc09e5405944a6319baf5e90335f221d5b91d44f5212c05bb1e751b997cc74db6f5d55f5861618351ec186'
        bhBytes = headerStr.decode('hex')

        hash357369 = 0x000000000000000007f379bc159a38fa5ccec4689336f32eba9d148b5c190439
        assert dblSha256Flip(bhBytes) == hash357369

        assert self.c.storeBlockHeader(bhBytes) == height + 1
        assert self.c.getBlockchainHead() == hash357369
        assert self.c.getLastBlockHeight() == height + 1
        assert self.c.getCumulativeDifficulty() == 1981795846593359


    def testStoreExistingHeader(self):
        res = self.storeGenesisBlock()
        g1 = res['gas']
        print('GAS: %s' % g1)
        assert res['output'] == 1

        res = self.storeGenesisBlock()
        g2 = res['gas']
        print('GAS: %s' % g2)
        assert res['output'] == 0 # no block stored
        assert g2 < 0.36 * g1  # 0.36 is as of aae201c


    def testStoreBlockHeader(self):
        block300K = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        self.c.setInitialParent(block300K, 299999, 1)

        # version = 2
        # hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        # hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
        # time = 1417792088
        # bits = 0x181b7b74
        # nonce = 796195988
        # blockNumber = 333001
        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBytes, profiling=True, sender=tester.k1)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        blockHash = self.c.getBlockchainHead()
        res = self.c.getBlockHeader(blockHash, profiling=True)
        print('GAS: %s' % res['gas'])
        assert res['output'] == bhBytes


    def testComputeMerkle(self):
        # values are from block 100K
        txHash = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49

        res = self.c.computeMerkle(txHash, txIndex, sibling, profiling=True)
        print('GAS: '+str(res['gas']))
        expMerkle = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        wrappedMerkle = res['output'] % 2**256
        assert wrappedMerkle == expMerkle

    def testsetInitialParentOnlyOnce(self):
        assert self.c.setInitialParent(0, 0, 1) == 1
        assert self.c.setInitialParent(0, 0, 1) == 0
