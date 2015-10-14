from ethereum import tester, exceptions

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

        expPayWei = 15
        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        bhBytes = blockHeaderStr.decode('hex')
        res = self.c.storeBlockWithFee(bhBytes, expPayWei, profiling=True, sender=tester.k1)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        blockHash = self.c.getBlockchainHead()
        res = self.c.getBlockHeader(blockHash, profiling=True)
        print('GAS: %s' % res['gas'])
        assert res['output'] == bhBytes

        #
        # test m_getFeeInfo which implicitly tests m_setFeeInfo
        #
        feeInfo = self.c.funcGetFeeInfo(blockHash)
        feeRecipient = feeInfo / 2**(12*8)
        feeWei = 0x0000000000000000000000000000000000000000ffffffffffffffffffffffff & feeInfo

        assert feeRecipient == int(tester.a1.encode('hex'), 16)
        assert feeWei == expPayWei

        #
        # test feePaid
        #
        balRecipient = self.s.block.get_balance(tester.a1)
        assert self.c.feePaid(blockHash, value=0) == 0
        assert self.s.block.get_balance(tester.a1) == balRecipient

        assert self.c.feePaid(blockHash, value=expPayWei-1) == 0
        assert self.s.block.get_balance(tester.a1) == balRecipient

        toPay = expPayWei
        assert self.c.feePaid(blockHash, value=toPay) == 1
        assert self.s.block.get_balance(tester.a1) == balRecipient + toPay
        balRecipient += toPay

        toPay = expPayWei+1
        assert self.c.feePaid(blockHash, value=toPay) == 0
        assert self.s.block.get_balance(tester.a1) == balRecipient

        toPay = expPayWei + int(10e18)  # 10 ETH extra
        assert self.c.feePaid(blockHash, value=toPay) == 0
        assert self.s.block.get_balance(tester.a1) == balRecipient

        with pytest.raises(exceptions.InsufficientBalance):
            self.c.feePaid(blockHash, value=2**256-1)

        with pytest.raises(exceptions.InvalidTransaction):
            self.c.feePaid(blockHash, value=2**256)

        #
        # change fee recipient
        #
        nextRec = int(tester.a2.encode('hex'), 16)
        nextFee = expPayWei+1
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=expPayWei) == 0

        nextFee = expPayWei
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee) == 0
