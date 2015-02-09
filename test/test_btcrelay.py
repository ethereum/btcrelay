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


    # http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
    def testTargetFromBits(self):
        bits = 0x19015f53
        exp = 8614444778121073626993210829679478604092861119379437256704
        res = self.c.targetFromBits(bits)
        assert res == exp
