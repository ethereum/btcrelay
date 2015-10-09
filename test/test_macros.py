from ethereum import tester

import datetime
import struct
import pytest
slow = pytest.mark.slow

from utilRelay import getHeaderBytes, dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestBtcRelay(object):
    CONTRACT_DEBUG = 'test/btcrelay_macros.se'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(3.3e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def testStoringHeader(self):
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

        assert self.c.funcPrevBlock(blockHash) == block300K
        assert self.c.funcGetTimestamp(blockHash) == 1417792088
        assert self.c.funcGetBits(blockHash) == 0x181b7b74


    # was converted to macro
    # def testFastHashBlock(self):
    #     blockHeaderStr = "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710"
    #     bhBytes = blockHeaderStr.decode('hex')
    #     res = self.c.fastHashBlock(bhBytes, profiling=True)
    #     print('GAS: '+str(res['gas']))
    #     exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
    #     assert res['output'] == exp


    def testTargetFromBits(self):
        bits = 0x19015f53
        exp = 8614444778121073626993210829679478604092861119379437256704
        assert self.c.funcTargetFromBits(bits) == exp

        bits = 453281356  # block100k
        exp = 0x000000000004864c000000000000000000000000000000000000000000000000
        assert self.c.funcTargetFromBits(bits) == exp

        maxTargetRounded = (2**16 - 1) * 2**208  # http://bitcoin.stackexchange.com/questions/8806/what-is-difficulty-and-how-it-relates-to-target
        bits = 0x1d00ffff  # EASIEST_DIFFICULTY_TARGET
        assert self.c.funcTargetFromBits(bits) == maxTargetRounded


    def testConcatHash(self):
        tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        r = self.c.funcConcatHash(tx1, tx2)
        assert r % 2**256 == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815
