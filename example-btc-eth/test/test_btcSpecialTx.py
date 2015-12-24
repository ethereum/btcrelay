from ethereum import tester
from datetime import datetime, date
import math

import pytest
slow = pytest.mark.slow

from utilRelay import dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestBtcSpecialTx(object):

    CONTRACT = 'example-btc-eth/btcSpecialTx.se'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    TX_STR = '010000000158115acce0e68bc58ecb89e6452380bd68da56dc0a163d9806c04b24dfefe269000000008a47304402207a0bf036d5c78d6910d608c47c9e59cbf5708df51fd22362051b8f1ecd9691d1022055ee6ace9f12f02720ce91f62916570dbd93b2aa1e91be7da8e5230f62606db7014104858527cb6bf730cbd1bcf636bc7e77bbaf0784b9428ec5cca2d8378a0adc75f5ca893d14d9db2034cbb7e637aacf28088a68db311ff6f1ebe6d00a62fed9951effffffff0210980200000000001976a914a0dc485fc3ade71be5e1b68397abded386c0adb788ac10270000000000001976a914d3193ccb3564d5425e4875fe763e26e2fce1fd3b88ac00000000'
    # TX_STR = '01 00 00 00 01 58115acce0e68bc58ecb89e6452380bd68da56dc0a163d9806c04b24dfefe269000000008a47304402207a0bf036d5c78d6910d608c47c9e59cbf5708df51fd22362051b8f1ecd9691d1022055ee6ace9f12f02720ce91f62916570dbd93b2aa1e91be7da8e5230f62606db7014104858527cb6bf730cbd1bcf636bc7e77bbaf0784b9428ec5cca2d8378a0adc75f5ca893d14d9db2034cbb7e637aacf28088a68db311ff6f1ebe6d00a62fed9951effffffff0210980200000000001976a914a0dc485fc3ade71be5e1b68397abded386c0adb788ac10270000000000001976a914d3193ccb3564d5425e4875fe763e26e2fce1fd3b88ac00000000'
    TX_BYTES = TX_STR.decode('hex');

    def setup_class(cls):
        tester.gas_limit = 2 * 10**6
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed

    def testGetUnsignedBitsLE(self):
        assert self.c.getUnsignedBitsLE('23', 0, 8) == [1, 0x23]
        assert self.c.getUnsignedBitsLE('45', 0, 8) == [1, 0x45]
        assert self.c.getUnsignedBitsLE('2345', 0, 16) == [2, 0x4523]
        assert self.c.getUnsignedBitsLE('012345', 0, 24) == [3, 0x452301]
        assert self.c.getUnsignedBitsLE('012345', 1, 16) == [2, 0x4523]
        assert self.c.getUnsignedBitsLE('01234567', 1, 16) == [2, 0x4523]
        assert self.c.getUnsignedBitsLE('01234567', 0, 32) == [4, 0x67452301]
        assert self.c.getUnsignedBitsLE('01234567', 2, 8) == [1, 0x45]
        assert self.c.getUnsignedBitsLE('01234567', 2, 16) == [2, 0x6745]
        assert self.c.getUnsignedBitsLE('0123456789abcdef', 0, 64) == [8, 0xefcdab8967452301]
        assert self.c.getUnsignedBitsLE('0123456789abcdef', 4, 32) == [4, 0xefcdab89]

    def testGetBytesLE(self):
        # assert self.c.getBytes('2345'.decode('hex'), 0, 16) == 0x23
        # assert self.c.getBytes('2345'.decode('hex'), 1, 16) == 0x45
        # assert self.c.getBytes('012345'.decode('hex'), 0, 16) == 0x01
        # assert self.c.getBytes('012345'.decode('hex'), 1, 16) == 0x23
        # assert self.c.getBytes('012345'.decode('hex'), 2, 16) == 0x45
        # assert 0

        assert self.c.getBytes('23'.decode('hex'), 0, 8) == [1, 0x23]
        assert self.c.getBytes('45'.decode('hex'), 0, 8) == [1, 0x45]
        assert self.c.getBytes('2345'.decode('hex'), 0, 16) == [2, 0x4523]
        assert self.c.getBytes('012345'.decode('hex'), 1, 16) == [2, 0x4523]
        assert self.c.getBytes('01234567'.decode('hex'), 1, 16) == [2, 0x4523]
        assert self.c.getBytes('01234567'.decode('hex'), 0, 32) == [4, 0x67452301]
        # assert self.c.getBytes('01234567'.decode('hex'), 2, 8) == [1, 0x45]
        assert self.c.getBytes('01234567'.decode('hex'), 2, 16) == [2, 0x6745]
        assert self.c.getBytes('0123456789abcdef'.decode('hex'), 0, 64) == [8, 0xefcdab8967452301]
        assert self.c.getBytes('0123456789abcdef'.decode('hex'), 4, 32) == [4, 0xefcdab89]
        # assert self.c.getBytes('012345'.decode('hex'), 0, 24) == [3, 0x452301]  bits 24 is not used


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

    def testGetVersion(self):
        res = self.c.parseBytes(self.TX_BYTES)
        assert res == 1
