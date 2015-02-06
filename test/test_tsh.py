from pyethereum import tester
from datetime import datetime, date

import pytest
slow = pytest.mark.slow

class TestBtcTx(object):

    CONTRACT = 'tryStoreHeaders.py'
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


    @slow
    # @pytest.mark.skipif(True,reason='skip')
    def test2(self):
        heaviest = 66
        self.c.initAncestorDepths()

        for i in range(1, heaviest+1):
          self.c.testStoreB(i, i, i-1)
        self.c.testSetHeaviest(heaviest)

        # # self.c.testStoreB(30, 30, 2)
        # # self.c.testStoreB(31, 31, 30)
        # # self.c.testStoreB(32, 32, 31)


        for i in range(1, heaviest+1):
            self.c.logAnc(i)

        # # self.c.logAnc(63)
        # # self.c.logAnc(64)
        # # self.c.logAnc(65)
        # # self.c.logAnc(66)
        #
        # self.c.logBlockchainHead()
