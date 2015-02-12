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
