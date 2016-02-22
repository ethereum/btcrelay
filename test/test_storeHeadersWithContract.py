from ethereum import tester
import pytest
slow = pytest.mark.slow

# from utilRelay import getHeaderBytes, argsForVerifyTx, dblSha256Flip, disablePyethLogging
from utilRelay import dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestStoreHeadersWithContract(object):
    CONTRACT_DEBUG = 'test/btcrelay_debug.se'

    def setup_class(cls):
        tester.gas_limit = int(2.7e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG)

        with open('test/headerSubmitter.sol') as solFile:
            cls.submitter = cls.s.abi_contract(solFile.read(), language='solidity')

        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    # based on testVerifyRequiresFee
    def testPaymentRejector(self):
        feeWei = 15
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.submitter.storeHeaderWithFee(blockHeaderBytes[i], feeWei, self.c.address)
            # print('@@@@ real chain score: ' + str(self.c.getChainWork()))
            assert res == i+100000

        chainWork = self.c.getChainWork()

        # block hashes
        b0 = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        b1 = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090 # block #100001
        b2 = 0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
        b3 = 0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1
        b4 = 0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79
        b5 = 0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45
        b6 = 0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60

        # values are from block 100K
        rawTx = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff08044c86041b020602ffffffff0100f2052a010000004341041b0e8c2567c12536aa13357b79a073dc4444acb83c4ec7a0e2f99dd7457516c5817242da796924ca4e99947d087fedf9ce467cb9f7c6287078f801df276fdf84ac00000000'.decode('hex')
        txHash = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        assert dblSha256Flip(rawTx) == txHash
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49

        assert self.c.getFeeRecipient(b0) == int(self.submitter.address.encode('hex'), 16)
        nextRec = int(tester.a0.encode('hex'), 16)
        assert self.c.changeFeeRecipient(b0, feeWei-1, nextRec, value=self.c.getChangeRecipientFee())
        assert self.c.getFeeRecipient(b0) == nextRec
        assert self.c.getFeeAmount(b0) == feeWei - 1

        txBlockHash = b0
        res = self.c.verifyTx(rawTx, txIndex, sibling, txBlockHash, value=feeWei)
        # actually don't reach here since TransactionFailed is thrown (tester.py line 201)
        assert res == 0  # contract rejecting payment prevents verifications from happening


    # based on testVerifyIsFee
    def testVerifyRequiresFee(self):
        feeWei = 15
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockWithFee(blockHeaderBytes[i], feeWei, sender=tester.k1)
            # print('@@@@ real chain score: ' + str(self.c.getChainWork()))
            assert res == i+100000

        chainWork = self.c.getChainWork()

        # block hashes
        b0 = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        b1 = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090 # block #100001
        b2 = 0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
        b3 = 0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1
        b4 = 0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79
        b5 = 0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45
        b6 = 0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60

        # values are from block 100K
        rawTx = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff08044c86041b020602ffffffff0100f2052a010000004341041b0e8c2567c12536aa13357b79a073dc4444acb83c4ec7a0e2f99dd7457516c5817242da796924ca4e99947d087fedf9ce467cb9f7c6287078f801df276fdf84ac00000000'.decode('hex')
        txHash = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        assert dblSha256Flip(rawTx) == txHash
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49

        assert self.c.getFeeRecipient(b0) == int(tester.a1.encode('hex'), 16)
        nextRec = int(tester.a0.encode('hex'), 16)
        assert self.c.changeFeeRecipient(b0, feeWei-1, nextRec, value=self.c.getChangeRecipientFee())
        assert self.c.getFeeRecipient(b0) == nextRec
        assert self.c.getFeeAmount(b0) == feeWei - 1

        # verifyTx should only return 1 for b0
        txBlockHash = b0
        res = self.c.verifyTx(rawTx, txIndex, sibling, txBlockHash, value=feeWei)
        assert res == txHash


    # based on testVerifyRawTx in test_btcrelay.py
    def testVerifyIsFree(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.submitter.storeHeader(blockHeaderBytes[i], self.c.address)
            # print('@@@@ real chain score: ' + str(self.c.getChainWork()))
            assert res == i+100000

        chainWork = self.c.getChainWork()

        # block hashes
        b0 = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        b1 = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090 # block #100001
        b2 = 0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
        b3 = 0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1
        b4 = 0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79
        b5 = 0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45
        b6 = 0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60

        # values are from block 100K
        rawTx = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff08044c86041b020602ffffffff0100f2052a010000004341041b0e8c2567c12536aa13357b79a073dc4444acb83c4ec7a0e2f99dd7457516c5817242da796924ca4e99947d087fedf9ce467cb9f7c6287078f801df276fdf84ac00000000'.decode('hex')
        txHash = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        assert dblSha256Flip(rawTx) == txHash
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49


        # verifyTx should only return 1 for b0
        txBlockHash = b0
        res = self.c.verifyTx(rawTx, txIndex, sibling, txBlockHash)
        assert res == txHash
