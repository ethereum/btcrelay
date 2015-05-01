from pyethereum import tester

import datetime
import struct
import pytest
slow = pytest.mark.slow

from utilRelay import dblSha256Flip

class TestBtcRelay(object):

    CONTRACT = 'btcrelay.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(2.2e6)
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed



    def getBlockHeaderBinary(self, ver, prev_block, mrkl_root, time_, bits, nonce):
        bytesPrevBlock = format(prev_block, '64x').replace(' ', '0')
        bytesPrevBlock = bytesPrevBlock.decode('hex')[::-1]

        bytesMerkle = format(mrkl_root, '64x').replace(' ', '0')
        bytesMerkle = bytesMerkle.decode('hex')[::-1]

        header = ( struct.pack("<L", ver) + bytesPrevBlock +
              bytesMerkle + struct.pack("<LLL", time_, bits, nonce))
        return header

    # also tests a (fake) fork
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
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
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
        # using script/mine.py these are the next 7 blocks
        # nonce: 0 blockhash: 11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        # nonce: 0 blockhash: 02c67135bd91986f9aaf3f0818baab439202fe5c34400c2c10bff6cd1336d436
        # nonce: 1 blockhash: 6e60065cc981914c23897143c75f0cde6e456df65f23afd41ddc6e6ce86b2b63
        # nonce: 1 blockhash: 38a052cdf4ef0fddf2de88e687163db7f39cb8de738fa9f5e871a72fc74c57c1
        # nonce: 0 blockhash: 2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c
        EASIEST_DIFFICULTY_TARGET = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = EASIEST_DIFFICULTY_TARGET
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBinary = self.getBlockHeaderBinary(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(blockHeaderBinary)
            hashPrevBlock = dblSha256Flip(blockHeaderBinary)

            # print('@@@@ fake chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000

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
        EASIEST_DIFFICULTY_TARGET = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = EASIEST_DIFFICULTY_TARGET
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBinary = self.getBlockHeaderBinary(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(blockHeaderBinary)
            hashPrevBlock = dblSha256Flip(blockHeaderBinary)
            assert res == i+100000

        # testingonlySetHeaviest is needed because the difficulty from
        # EASIEST_DIFFICULTY_TARGET becomes 0 and so the score does not
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
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        block100k = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
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
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
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
            res = self.c.within6Confirms(bh)
            exp = 0 if i==0 else 1
            assert res == exp


    def storeGenesisBlock(self):
        self.c.setInitialParent(0, 0, 1)

        blockHeaderStr = ("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBinary, profiling=True)
        return res

    def storeBlock1(self):
        # block 1
        blockHeaderStr = ("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299")
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBinary, profiling=True)
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
        bhBinary = blockHeaderStr.decode('hex')

        assert self.c.storeBlockHeader(bhBinary) == 300000

    # was converted to macro
    # def testFastHashBlock(self):
    #     blockHeaderStr = "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710"
    #     bhBinary = blockHeaderStr.decode('hex')
    #     res = self.c.fastHashBlock(bhBinary, profiling=True)
    #     print('GAS: '+str(res['gas']))
    #     exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
    #     assert res['output'] == exp

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
