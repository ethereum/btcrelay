from ethereum import tester

import datetime
import struct
import json
from functools import partial
import pytest
slow = pytest.mark.slow

from utilRelay import getHeaderBytes, argsForVerifyTx, dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestFee(object):
    CONTRACT_DEBUG = 'test/btcrelay_fee.se'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(3e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def testBlockWithFee(self):
        block300K = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        self.c.setInitialParent(block300K, 299999, 1)

        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockWithFee(bhBytes, 15, profiling=True, sender=tester.k1)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        blockHash = self.c.getBlockchainHead()
        res = self.c.getBlockHeader(blockHash, profiling=True)
        print('GAS: %s' % res['gas'])
        assert res['output'] == bhBytes
