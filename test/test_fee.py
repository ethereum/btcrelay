from ethereum import tester, exceptions

import datetime
import struct
import json
from functools import partial
import pytest
slow = pytest.mark.slow

from utilRelay import makeMerkleProof, randomMerkleProof, \
    getHeaderBytes, dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestFee(object):
    CONTRACT_DEBUG = 'test/btcrelay_fee.se'

    FEE_VERIFY_TX = 255

    def setup_class(cls):
        tester.gas_limit = int(3e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    # based on https://github.com/ethers/btcrelay/blob/4fca910ca4d5d95c0a6b6d1a8c75b2d5a942e113/test/test_tokens.py#L65
    def testChargeOneVerifyTx(self):
        numHeader = 24  # minimum is 24 (block 300017 plus 6 confirmations)
        keySender = tester.k1
        addrSender = tester.a1
        self.storeHeadersFrom300K(numHeader, keySender, addrSender)

        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, 1)

        assert self.c.getFee(txBlockHash) == self.FEE_VERIFY_TX
        assert self.c.getFeeRecipient(txBlockHash) == int(addrSender.encode('hex'), 16)

        # eventArr = []
        # self.s.block.log_listeners.append(lambda x: eventArr.append(self.c._translator.listen(x)))


        senderBal = self.s.block.get_balance(addrSender)
        balCaller = self.s.block.get_balance(tester.a0)
        res = self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=tester.k0, value=self.FEE_VERIFY_TX, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == 1  # adjust according to numHeader and the block that the tx belongs to

        senderBal += self.FEE_VERIFY_TX
        balCaller -= self.FEE_VERIFY_TX
        assert self.s.block.get_balance(addrSender) == senderBal
        assert self.s.block.get_balance(tester.a0) == balCaller

        # assert eventArr == [{'_event_type': 'ethPayment'}]
        # eventArr.pop()


        #
        # zero payment
        #
        assert 0 == self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=tester.k0, value=0)
        assert self.s.block.get_balance(addrSender) == senderBal
        assert self.s.block.get_balance(tester.a0) == balCaller

        #
        # insufficient payment is burned to contract
        #
        balCaller -= self.FEE_VERIFY_TX - 1
        assert 0 == self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=tester.k0, value=self.FEE_VERIFY_TX-1)
        assert self.s.block.get_balance(addrSender) == senderBal
        assert self.s.block.get_balance(tester.a0) == balCaller
        assert self.s.block.get_balance(self.c.address) == self.FEE_VERIFY_TX - 1

        #
        # overpayment is burned to contract
        #
        balCaller -= self.FEE_VERIFY_TX + 1
        assert 0 == self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, sender=tester.k0, value=self.FEE_VERIFY_TX+1)
        assert self.s.block.get_balance(addrSender) == senderBal
        assert self.s.block.get_balance(tester.a0) == balCaller
        assert self.s.block.get_balance(self.c.address) == self.FEE_VERIFY_TX * 2



    def storeHeadersFrom300K(self, numHeader, keySender, addrSender):
        startBlockNum = 300000

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        i = 1
        feeWei = self.FEE_VERIFY_TX
        with open("test/headers/100from300k.txt") as f:
            for header in f:
                res = self.c.storeBlockWithFee(header[:-1].decode('hex'), feeWei, sender=keySender)  # [:-1] to remove \n
                assert res == i-1+startBlockNum

                if i==numHeader:
                    break
                i += 1


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
        prevFee = expPayWei
        nextFee = prevFee+1  # fee increase should not be allowed
        print('@@@ expPayWei: ' + str(expPayWei))
        balNextRec = self.s.block.get_balance(tester.a2)
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee+1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee+999, nextRec, value=nextFee+1000) == 0

        balRecipient += prevFee  # disallowed overpayment is NOT refunded
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=prevFee) == 0
        assert self.s.block.get_balance(tester.a1) == balRecipient

        nextFee = prevFee  # equal fee should not be allowed since fees should be decreasing
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec) == 0

        balRecipient += prevFee  # disallowed overpayment is NOT refunded
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee) == 0
        assert self.s.block.get_balance(tester.a1) == balRecipient

        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee+1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee+1000) == 0

        nextFee = prevFee-1
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee) == 0
        # assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee+1) == 1  same as paying prevFee below
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=nextFee+1000) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=prevFee+1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=prevFee-1) == 0

        balRecipient += prevFee
        assert self.c.changeFeeRecipient(blockHash, nextFee, nextRec, value=prevFee) == 1
        assert self.s.block.get_balance(tester.a1) == balRecipient

        assert self.s.block.get_balance(tester.a2) == balNextRec

        #
        # decrease fee to 1 wei
        #
        prevFee = nextFee
        thirdRec = int(tester.a3.encode('hex'), 16)
        balThirdRec = self.s.block.get_balance(tester.a3)
        nextFee = 1
        assert self.c.changeFeeRecipient(blockHash, nextFee, thirdRec) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, thirdRec, value=prevFee-1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, thirdRec, value=prevFee+1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, thirdRec, value=prevFee+1000) == 0

        balNextRec += prevFee
        assert self.c.changeFeeRecipient(blockHash, nextFee, thirdRec, value=prevFee) == 1
        assert self.s.block.get_balance(tester.a2) == balNextRec

        assert self.s.block.get_balance(tester.a3) == balThirdRec

        #
        # decrease fee to 0
        #
        prevFee = nextFee
        fourthRec = int(tester.a3.encode('hex'), 16)
        balFourthRec = self.s.block.get_balance(tester.a4)
        nextFee = 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, fourthRec) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, fourthRec, value=prevFee-1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, fourthRec, value=prevFee+1) == 0
        assert self.c.changeFeeRecipient(blockHash, nextFee, fourthRec, value=prevFee+1000) == 0

        balThirdRec += prevFee
        assert self.c.changeFeeRecipient(blockHash, nextFee, fourthRec, value=prevFee) == 1
        assert self.s.block.get_balance(tester.a3) == balThirdRec

        assert self.s.block.get_balance(tester.a4) == balFourthRec
