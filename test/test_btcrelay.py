from pyethereum import tester

import datetime
import pytest
slow = pytest.mark.slow

class TestBtcTx(object):

    CONTRACT = 'btcrelay.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed



    def testHeadersFrom100K(self):
        block100k = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        self.c.testingonlySetHeaviest(block100k)

        # 100k + 1
        rawBlockHeader = "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b"
        res = self.c.storeRawBlockHeader(rawBlockHeader)

        # repeat
        #


        # values are from block 100K
        # tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        # proofLen = 2
        # hash = array(proofLen)
        # path = array(proofLen)
        #
        # hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        # path[0] = RIGHT_HASH
        #
        # hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
        # path[1] = RIGHT_HASH
        #
        # # txBlockHash = 0xdead
        # # expFake = 0 == self.verifyTx(tx, proofLen, hash, path, txBlockHash)
        # #
        # # txBlockHash = b1
        # # expB1 = 0 == self.verifyTx(tx, proofLen, hash, path, txBlockHash)
        #
        # # verifyTx should only return 1 for b0
        # txBlockHash = b0
        # res = self.c.verifyTx(tx, proofLen, hash, path, txBlockHash)
        # assert res == 1





    def testStoreBlockHeader(self):
        self.c.init333k()
        version = 2
        hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
        time = 1417792088
        bits = 0x181b7b74
        nonce = 796195988
        blockNumber = 333001

        assert blockNumber == self.c.storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)

    def testComputeMerkle(self):
        # values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        proofLen = 2
        hash = [None] * proofLen
        path = [None] * proofLen

        RIGHT_HASH = 2  # from btcrelay.py

        hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        path[0] = RIGHT_HASH

        hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
        path[1] = RIGHT_HASH

        r = self.c.computeMerkle(tx, proofLen, hash, path)
        expMerkle = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        return(r == expMerkle)


    # @pytest.mark.skipif(True,reason='skip')
    def testHashHeader(self):
        version = 2
        hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
        time = 1417792088
        bits = 0x181b7b74
        nonce = 796195988

        expBlockHash = 0x000000000000000010e318d0c61da0b84246481d9cc097fda9327fe90b1538c1
        blockHash = self.c.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        assert blockHash == expBlockHash



    # @pytest.mark.skipif(True,reason='skip')
    def testDoRawHashBlockHeader(self):
        # https://en.bitcoin.it/wiki/Block_hashing_algorithm
        version = 0x01000000
        hashPrevBlock = 0x81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000
        hashMerkleRoot = 0xe320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b
        time = 0xc7f5d74d
        bits = 0xf2b9441a
        nonce = 0x42a14695

        # these should be the intermediate b1,b2,b3 values inside doRawHashBlockHeader()
        # b1 = 0x0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
        # b2 = 0x00000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
        # b3 = 0xf1fc122bc7f5d74df2b9441a42a1469500000000000000000000000000000000
        # hash1 = sha256([b1,b2,b3], chars=80)
        # hash2 = sha256([hash1], 1)
        # return(hash2)

        res = self.c.doRawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        # log(res)

        expHash = 0x1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000
        assert res == expHash


    # @pytest.mark.skipif(True,reason='skip')
    def testIsNonceValid(self):
        ver = 2
        prev_block = 0x000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717
        mrkl_root = 0x871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a
        time_ = 0x53058b35 # 2014-02-20 04:57:25
        bits = 0x19015f53
        nonce = 856192328

        res = self.c.isNonceValid(ver, prev_block, mrkl_root, time_, bits, nonce)
        assert res == 1

    def testConcatHash(self):
        tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        r = self.c.concatHash(tx1, tx2)
        r = r % 2 ** 256
        assert r == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815


    # http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
    def testTargetFromBits(self):
        bits = 0x19015f53
        exp = 8614444778121073626993210829679478604092861119379437256704
        res = self.c.targetFromBits(bits)
        assert res == exp
