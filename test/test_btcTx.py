from pyethereum import tester

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

    @slow
    def testSB(self):
        assert self.c.testStoringHeaders() == [2]
