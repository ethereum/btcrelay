from pyethereum import tester
from datetime import datetime, date
import math

import pytest
slow = pytest.mark.slow

class TestBtcSpecialTx(object):

    CONTRACT = 'btcSpecialTx.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = 2 * 10**6
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def test_testnetTx(self):
        # testnet tx a51a71f8094f9b4e266fcccd55068e809277ec79bfa44b7bdb8f1355e9bb8460
        #    tx[9] of block 350559
        txStr = '010000000158115acce0e68bc58ecb89e6452380bd68da56dc0a163d9806c04b24dfefe269000000008a47304402207a0bf036d5c78d6910d608c47c9e59cbf5708df51fd22362051b8f1ecd9691d1022055ee6ace9f12f02720ce91f62916570dbd93b2aa1e91be7da8e5230f62606db7014104858527cb6bf730cbd1bcf636bc7e77bbaf0784b9428ec5cca2d8378a0adc75f5ca893d14d9db2034cbb7e637aacf28088a68db311ff6f1ebe6d00a62fed9951effffffff0210980200000000001976a914a0dc485fc3ade71be5e1b68397abded386c0adb788ac10270000000000001976a914d3193ccb3564d5425e4875fe763e26e2fce1fd3b88ac00000000'
        res = self.c.getFirst2Outputs(txStr)
        assert res[0] == 170000

        out1stScriptIndex = res[1]
        btcAddrIndex = out1stScriptIndex*2 + 6
        assert txStr[btcAddrIndex:btcAddrIndex+40] == 'a0dc485fc3ade71be5e1b68397abded386c0adb7'

        out2ndScriptIndex = res[2]
        ethAddrIndex = out2ndScriptIndex*2 + 6
        assert txStr[ethAddrIndex:ethAddrIndex+40] == 'd3193ccb3564d5425e4875fe763e26e2fce1fd3b'
