from ethereum import tester

import datetime
import struct
import json
from functools import partial
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


    # fork at block 363731
    def testForkingPast(self):
        forkGrandParent = 0x000000000000000011e40c5deb1a1e3438b350ea3db3fa2dedd285db9650a6e6
        forkPrevHash = 0x000000000000000006a320d752b46b532ec0f3f815c5dae467aff5715a6e579e
        forkPrevNum = 363730
        self.c.setInitialParent(forkGrandParent, forkPrevNum-1, 1)

        forkPrevHashHeader = "03000000e6a65096db85d2ed2dfab33dea50b338341e1aeb5d0ce411000000000000000098420532fa55a0bca5f043f8f8f16a2b73761e822178692cb99ced039e2a32a0ea3f97558e4116183a9cc34a"
        assert self.c.storeBlockHeader(forkPrevHashHeader.decode('hex')) == forkPrevNum

        # insert the 6 blocks from the fork that will be orphaned
        b0 = forkPrevHash
        b1 = 0
        b6 = 0
        hashPrevBlock = forkPrevHash
        for i in range(1, 7):
            with open('test/headers/fork/20150704/36373'+str(i)+'.json') as dataFile:
                blockJson = json.load(dataFile)
                # print blockJson['hash']

                version = blockJson['ver']
                assert int(blockJson['prev_block'], 16) == hashPrevBlock
                hashMerkleRoot = int(blockJson['mrkl_root'], 16)
                time = blockJson['time']
                bits = blockJson['bits']
                nonce = blockJson['nonce']

                blockHeaderBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
                res = self.c.storeBlockHeader(blockHeaderBytes)

                # set the next hashPrevBlock
                hashPrevBlock = int(blockJson['hash'], 16)
                assert hashPrevBlock == dblSha256Flip(blockHeaderBytes)

                b1 = hashPrevBlock if i==1 else b1
                b6 = hashPrevBlock if i==6 else b6

                # print('@@@@ chain score: ' + str(self.c.getCumulativeDifficulty()))
                assert res == i+forkPrevNum

        cumulDiff = self.c.getCumulativeDifficulty()
        assert cumulDiff == 49402014931*7 + 1  # 1 is the initial score

        # tx[1] of block 363730
        txIndex = 1
        txOne = 0xb58e45ee29d7ad51923855cc04f926e23fa0e0d9645b7326f97c31f9ec5ff983
        # the following was ran offline (since there are 135 txs in
        # block 363730 and bci rate limits) in a python console with bitcoin module imported
        # header = get_block_header_data(363730)
        # hashes = get_txs_in_block(363730)
        # merkleProof = mk_merkle_proof(header, hashes, txIndex)
        merkleProof = {'siblings': ['7db80bd2051a1e8e7b6186c60306e0d774600e23d37172ef24b4f21ede5c50bc', 'ff2323064d268d365f324fbf70bc514835f843ad4bb1bfa335e2b603895adb19', 'c4ed3cc5ba175cca50749b8a4cad5abc3cdeeec4d25aa66917924e2d6e22ec6c', '4c09b1d4255d334e507c42ebcf663cd25ca75faa02fcd490fab63d3a1f695f51', '572959e56447bbc8df6a2d6e9f89d340d60a8f99867a03de0816eff4f95b630b', '0c418846ad446e8b65fc8d0dd31fb3e6c72c4931062cfb0a4d3d34248630fec5', '1ddafddbd52b86ce9988c7b573af24fa4712c0504646c1d016da03e33adf5e00', '045ca7d0156bf1b136d884eada3d53286d2e6bedbe4e1f33699fa9172b469d06'], 'hash': u'b58e45ee29d7ad51923855cc04f926e23fa0e0d9645b7326f97c31f9ec5ff983', 'header': {'nonce': 1254333498, 'hash': u'000000000000000006a320d752b46b532ec0f3f815c5dae467aff5715a6e579e', 'timestamp': 1435975658, 'merkle_root': u'a0322a9e03ed9cb92c697821821e76732b6af1f8f843f0a5bca055fa32054298', 'version': 3, 'prevhash': u'000000000000000011e40c5deb1a1e3438b350ea3db3fa2dedd285db9650a6e6', 'bits': 404111758}}
        txHash = int(merkleProof['hash'], 16)
        sibling = map(partial(int,base=16), merkleProof['siblings'])
        txBlockHash = int(merkleProof['header']['hash'], 16)
        txInBlockZero = [txHash, txIndex, sibling, txBlockHash]

        assert txHash == txOne
        assert txBlockHash == b0


        # TODO
        # b1 is within6confirms so should NOT verify
        # txBlockHash = b1
        # res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        # assert res == 0


        # verifyTx should only return 1 for b0
        res = self.c.verifyTx(*txInBlockZero)
        assert res == 1

        assert b6 == self.c.getBlockchainHead()


        # insert the blocks that will cause reorg as main chain

        headers = [
            "030000009e576e5a71f5af67e4dac515f8f3c02e536bb452d720a306000000000000000022862bfc426ccbe5868e8ee0d0abb9e89aa86a6031fa597323a081dcb29b15cff54897558e4116184b082d3b",
            "0300000053ef2a88b2b244409f03fee87f819ef14690c23033e2280c00000000000000009e90b9ad092c3f37393f163f70fcc054cbc7dc38210f213840fa9cf9791493b3954997558e4116186d536b51",
            "03000000d691c32ec84e22c0b9c8fbec184c0ec5f113b16e21e04212000000000000000092ccf4a5399e2436948a6917471135340a51967704bff3c55e57f5f0af6ca7d4275397558e411618d0abe918",
            "03000000eea345978c6b095148670d6128e1cc9069ac6bb3075c35060000000000000000b00ecf72f6d247a60eca5fc70d760939139cc0bc008d483c90b43e22596e0ed1dc5497558e41161884e655a3",
            "0300000036191cd0a5e5b1f04dec4cbb97170883fa621013e18a35150000000000000000d8f418aa2714981e26938ccd1620649a5c6fbe839eabc133ac0fac49deafe7dcb75597558e41161810d85d32",
            "03000000deab448a286a2873fcb3eac032aa1fbb13b7c96a3f24950600000000000000005df3fffaf0b0d3db741bf96cbf35830e3497f0634c819779281b4a2e5d301d65cd5697558e411618983a2772",

            "0300000033c784021ffbbdfff3bea3b4b9a7caa7f4f8c60713f7bc0300000000000000006e28294eb3195a9fe49845bd090bd69afe1e2b9301a8da1c27fd14a819d86da9a25797558e4116181625905a"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(6):  # only 6 blocks first
            res = self.c.storeBlockHeader(blockHeaderBytes[i])
            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+1+forkPrevNum

        assert self.c.getCumulativeDifficulty() == cumulDiff  # cumulDiff should not change
        assert self.c.getBlockchainHead() == dblSha256Flip(blockHeaderBytes[-2])

        # tx[1] block 363731
        # Ran this offline since many txs in 363731
        # merkleProof = merkle_prove('fcf7daef2123a30a472e3ee9358b950e684f5a61af61295f06688a283f1d1cd7')
        merkleProof = {'siblings': ['2587cd4d66c1baaba5d4534ff84f4880d7cc14f399c9ebffd5527b4e5fc88870', '41cdaf2bd64ca88648eeb2529e9ef594a40d83e26d048ddee815c8a36aa470e1', '22e557f4c63fd85683a949064add7397c22121e371b5617ef1063dda063fe9c9', 'a3d258a75fcb7df2d9e1904236888fa2a50b139f9146ea60f78716e6240947fc', 'c6ef6fe56abb6d1cbbe042bf1fb304bb708a1f05a4805c451e3680b671c01a7d', '30b0f61f406f37346f002d9eed518dd22aed68c111c3e6543d013703813f2662', '26ec8b0a87da3335f773c35c308c85867733f7e93c185c164aab3f9d3e42730a', '31535344a3d72372df8321540c38f58881d6e49b0b64a69a9bf2b80fa4e31c0f', '96e441b6876b3f72394b4c1e5e4f851df4ba4cd186801879b13873183bbb1968', 'c23c775e159c2af628e4a90d4657557b2cb15212e0ef3b23caf1187e8d779646', 'c6a1286ef43a26b5f9bed22ddad0d9fcae79fb380bdeb43236e8f41e1deab13f'], 'hash': u'fcf7daef2123a30a472e3ee9358b950e684f5a61af61295f06688a283f1d1cd7', 'header': {'nonce': 992806987, 'hash': u'00000000000000000c28e23330c29046f19e817fe8fe039f4044b2b2882aef53', 'timestamp': 1435977973, 'merkle_root': u'cf159bb2dc81a0237359fa31606aa89ae8b9abd0e08e8e86e5cb6c42fc2b8622', 'version': 3, 'prevhash': u'000000000000000006a320d752b46b532ec0f3f815c5dae467aff5715a6e579e', 'bits': 404111758}}
        txHash = int(merkleProof['hash'], 16)
        sibling = map(partial(int,base=16), merkleProof['siblings'])
        txBlockHash = int(merkleProof['header']['hash'], 16)
        txInBlockOne = [txHash, txIndex, sibling, txBlockHash]

        res = self.c.verifyTx(*txInBlockOne)
        assert res == 0

        # b0 should still verify
        res = self.c.verifyTx(*txInBlockZero)
        assert res == 1

        #TODO add another header and txInBlockOne should pass verifyTx


    # TODO verify tx in b1
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
        # TODO use proper tx, txIndex, sibling.  Should also test that
        # when another header is added, the tx does verify
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
