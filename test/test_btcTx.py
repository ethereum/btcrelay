from pyethereum import tester

import datetime
import pytest
slow = pytest.mark.slow

class TestBtcTx(object):

    CONTRACT = 'btcTx.py'
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


    @pytest.mark.skipif(True,reason='skip')
    def testGenesis(self):
        rawBlockHeader = ("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
        res = self.c.storeRawBlockHeader(rawBlockHeader)
        assert res == [1]


    def test_getOutputScriptWithMultipleInputs(self):
        # 3 ins, 2 outs
        rawTx = ("0100000003d64e15b7c11f7532059fe6aacc819b5d886e3aaa602078db57cbae2a8f17cde8000000006b483045022027a176130ebf8bf49fdac27cdc83266a68b19c292b08df1be29f3d964c7e90b602210084ae66b4ff5ed342d78102ef8a4bde87b3ded06929ccaf9a8f71b137baa1816a012102270d473b083897519e5f01c47de7ac50877b6a295775f35966922b3571614370ffffffff54f0e7ded00c01082257eda035d65513b509ddbbe05fae19df0065c294822c9d010000006c493046022100f7423fdbcff22d3cd49921d0af92420d548b925bb1671dc826f15ccc5e05c3de022100d60a6178d892bcf012a79cf9e3430ab70a33b3fa2d156ecf541584e44fa83b150121036674d9607e0461b158c4b3d6368d1869e893cd122c68ebe47af253ff686f064effffffffa6155f8b449da0d3f9d2e1bc8e864c8b78615c1fa560076acaee8802d256a6dd010000006c493046022100e220318b55597c80eecccf9b84f37ab287c14277ccccd269d32f863d8d58d403022100f87818cbed15276f0d5be51aed5bd3b8dea934d6dd2244f2c3170369b96f365501210204b08466f452bb42cefc081ca1c773e26ce0a43566bd9d17b30065c1847072f4ffffffff02301bb50e000000001976a914bdb644fddd802bf7388df220279a18abdf65ebb788ac009ccf6f000000001976a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac00000000")
        outNum = 0
        # exp hash is untested
        expHashOfOutputScript = 56502271141207574289324577080259466406131090189524790551966501267826601078627
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == [1]


    @slow
    @pytest.mark.skipif(True,reason='skip')
    def testSB(self):
        print("jstart")
        i = 1
        with open("test/headers/bh80k.txt") as f:

            print("*************************"+str(datetime.datetime.now().time()))

            for header in f:
                # print(header)
                res = self.c.storeRawBlockHeader(header)
                if i==10:
                    break
                assert res == [i]
                i += 1

            print("*************************"+str(datetime.datetime.now().time()))

        # with open("test/headers/bh80_100k.txt") as f:
        #     for header in f:
        #         # print(header)
        #         res = self.c.storeRawBlockHeader(header)
        #         assert res == [i]
        #         i += 1
        #
        # with open("test/headers/bh100_150k.txt") as f:
        #     for header in f:
        #         # print(header)
        #         res = self.c.storeRawBlockHeader(header)
        #         assert res == [i]
        #         i += 1


        self.c.logBlockchainHead()

        print "gas used: ", self.s.block.gas_used
        print("jend")

        # h = "0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c"
        # res = self.c.storeRawBlockHeader(h)
        # assert res == [1]
