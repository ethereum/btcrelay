from ethereum import tester
import pytest
slow = pytest.mark.slow

# from utilRelay import getHeaderBytes, argsForVerifyTx, dblSha256Flip, disablePyethLogging
from utilRelay import disablePyethLogging

disablePyethLogging()


class TestStoreHeadersWithContract(object):
    CONTRACT_DEBUG = 'test/btcrelay_debug.se'

    def setup_class(cls):
        tester.gas_limit = int(2.7e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def testPaymentRejector(self):
        assert 1 == 2
