from pyethereum import tester
from datetime import datetime, date
from functools import partial

from utilRelay import makeMerkleProof, randomMerkleProof

import time

import pytest
slow = pytest.mark.slow



class TestTxVerify(object):

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


    # if txIndex is -1, randomly choose a tx index
    def randomTxVerify(self, blocknum, txIndex=-1, profiling=False):
        [txHash, siblings, path, txBlockHash] = randomMerkleProof(blocknum, txIndex)
        res = self.c.verifyTx(txHash, len(siblings), siblings, path, txBlockHash, profiling=profiling)
        return res


    @slow
    def test80from300K(self):
        startBlockNum = 300000
        numBlock = 80

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        i = 1
        with open("test/headers/100from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeBlockHeader(header[:-1].decode('hex'))  # [:-1] to remove trailing \n
                if i==numBlock:
                    break
                i += 1
                assert res == i

            endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))
        print "GAS: ", self.s.block.gas_used


    @slow
    @pytest.mark.veryslow
    # check params such as timeoutSecs
    def test400from300K(self):
        startBlockNum = 300000
        numBlock = 400

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        i = 1
        with open("test/headers/500from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeBlockHeader(header[:-1].decode('hex'))  # [:-1] to remove trailing \n
                if i==numBlock:
                    break
                i += 1
                assert res == i

            endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        nChecks = 40000
        timeoutSecs = 1  # may need longer to avoid termination by blockchain.info (BCI)
        for i in range(nChecks):
            if i > 20:
                time.sleep(timeoutSecs)
            if i%60 == 0:
                print('BCI nth check '+str(i))

            randBlock = random.randrange(startBlockNum, startBlockNum+numBlock)
            res = self.randomTxVerify(randBlock)

            # should only verify when more than 6 confirmations
            if randBlock < startBlockNum+numBlock-6:
                assert res == 1
            else:
                assert res == 0

    # tx[1] of block 100K sends enough BTC, so ether should be transferred
    def testRelayTx(self):
        BTC_ETH = self.s.abi_contract('btc-eth.py', endowment=2000*self.ETHER)
        BTC_ETH.setTrustedBtcRelay(self.c.address)

        #
        # store block headers
        #
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+2

        # tx[1] fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        txStr = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000'

        # block 100000
        header = {'nonce': 274148111, 'hash': u'000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506', 'timestamp': 1293623863, 'merkle_root': u'f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766', 'version': 1, 'prevhash': u'000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250', 'bits': 453281356}
        hashes = [u'8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87', u'fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4', u'6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4', u'e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d']
        [txHash, siblings, path, txBlockHash] = makeMerkleProof(header, hashes, 1)

        res = self.c.relayTx(txStr, txHash, len(siblings), siblings, path, txBlockHash, BTC_ETH.address, profiling=True)
        print('GAS: '+str(res['gas']))

        ethAddrBin = txStr[-52:-12].decode('hex')
        userEthBalance = self.s.block.get_balance(ethAddrBin)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 13
        assert userEthBalance == expEtherBalance
        assert res['output'] == 1  # ether was transferred

        assert 0 == self.c.relayTx(txStr, txHash, len(siblings), siblings, path, txBlockHash, BTC_ETH.address)  # re-claim disallowed



    # tx[2] of block 100K does NOT send enough BTC, so ether should NOT be transferred
    def testInsufficientBTCSent(self):
        BTC_ETH = self.s.abi_contract('btc-eth.py', endowment=2000*self.ETHER)
        BTC_ETH.setTrustedBtcRelay(self.c.address)

        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+2

        # tx[2] 6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4
        txStr = '0100000001c33ebff2a709f13d9f9a7569ab16a32786af7d7e2de09265e41c61d078294ecf010000008a4730440220032d30df5ee6f57fa46cddb5eb8d0d9fe8de6b342d27942ae90a3231e0ba333e02203deee8060fdc70230a7f5b4ad7d7bc3e628cbe219a886b84269eaeb81e26b4fe014104ae31c31bf91278d99b8377a35bbce5b27d9fff15456839e919453fc7b3f721f0ba403ff96c9deeb680e5fd341c0fc3a7b90da4631ee39560639db462e9cb850fffffffff0240420f00000000001976a914b0dcbf97eabf4404e31d952477ce822dadbe7e1088acc060d211000000001976a9146b1281eec25ab4e1e0793ff4e08ab1abb3409cd988ac00000000'

        # block 100000
        header = {'nonce': 274148111, 'hash': u'000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506', 'timestamp': 1293623863, 'merkle_root': u'f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766', 'version': 1, 'prevhash': u'000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250', 'bits': 453281356}
        hashes = [u'8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87', u'fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4', u'6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4', u'e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d']
        [txHash, siblings, path, txBlockHash] = makeMerkleProof(header, hashes, 2)

        res = self.c.relayTx(txStr, txHash, len(siblings), siblings, path, txBlockHash, BTC_ETH.address)

        ethAddrBin = txStr[-52:-12].decode('hex')
        userEthBalance = self.s.block.get_balance(ethAddrBin)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 0
        assert userEthBalance == expEtherBalance
        assert res == 0  # ether was NOT transferred


    def testEachConfirmation(self):
        BTC_ETH = self.s.abi_contract('btc-eth.py', endowment=2000*self.ETHER)
        BTC_ETH.setTrustedBtcRelay(self.c.address)

        # tx[1] fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        txStr = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000'

        # block 100000
        header = {'nonce': 274148111, 'hash': u'000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506', 'timestamp': 1293623863, 'merkle_root': u'f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766', 'version': 1, 'prevhash': u'000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250', 'bits': 453281356}
        hashes = [u'8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87', u'fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4', u'6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4', u'e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d']
        [txHash, siblings, path, txBlockHash] = makeMerkleProof(header, hashes, 1)

        ethAddrBin = txStr[-52:-12].decode('hex')
        expEtherBalance = 13

        #
        # store block headers
        #
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+2

            res = self.c.relayTx(txStr, txHash, len(siblings), siblings, path, txBlockHash, BTC_ETH.address)

            userEthBalance = self.s.block.get_balance(ethAddrBin)
            print('USER ETH BALANCE: '+str(userEthBalance))

            if (i==6):
                assert userEthBalance == expEtherBalance
                assert res == 1  # ether was transferred
            else:
                assert 0 == res == userEthBalance


    def test7BlockValidTx(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+2

        # block 100000
        header = {'nonce': 274148111, 'hash': u'000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506', 'timestamp': 1293623863, 'merkle_root': u'f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766', 'version': 1, 'prevhash': u'000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250', 'bits': 453281356}
        hashes = [u'8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87', u'fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4', u'6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4', u'e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d']
        [txHash, siblings, path, txBlockHash] = makeMerkleProof(header, hashes, 3)

        res = self.c.verifyTx(txHash, len(siblings), siblings, path, txBlockHash)
        assert res == 1  # adjust according to numBlock and the block that the tx belongs to


    def test30BlockValidTx(self):
        startBlockNum = 300000
        numBlock = 30

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        i = 1
        with open("test/headers/100from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeBlockHeader(header[:-1].decode('hex'))  # [:-1] to remove \n
                if i==numBlock:
                    break
                i += 1
                assert res == i

            endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, siblings, path, txBlockHash] = makeMerkleProof(header, hashes, 1)

        res = self.c.verifyTx(txHash, len(siblings), siblings, path, txBlockHash, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == 1  # adjust according to numBlock and the block that the tx belongs to


    @slow
    def testRandomTxVerify(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+2

        startBlockNum = 100000
        numBlock = 7
        for i in range(startBlockNum, startBlockNum+numBlock):
            res = self.randomTxVerify(i)
            if i < startBlockNum+numBlock-6:
                assert res == 1
            else:
                assert res == 0


    def randomTxMerkleCheck(self, blocknum):
        header = get_block_header_data(blocknum)
        hashes = get_txs_in_block(blocknum)

        numTx = len(hashes)
        if numTx == 0:
            print('@@@@ empty blocknum='+str(blocknum))
            return

        index = random.randrange(numTx)
        proof = mk_merkle_proof(header, hashes, index)

        print('@@@@@@@@@@@@@@@@ blocknum='+str(blocknum)+'\ttxIndex='+str(index))

        tx = int(hashes[index], 16)
        siblings = map(partial(int,base=16), proof['siblings'])
        nSibling = len(siblings)
        path = indexToPath(index, nSibling)
        merkle = self.c.computeMerkle(tx, len(siblings), siblings, path)
        merkle %= 2 ** 256
        assert merkle == int(proof['header']['merkle_root'], 16)

    @slow
    def testRandomTxMerkleCheck(self):
        self.randomTxMerkleCheck(100000)


    @pytest.mark.skipif(True,reason='skip')
    def testProof(self):
        blocknum = 100000
        header = get_block_header_data(blocknum)
        hashes = get_txs_in_block(blocknum)
        index = 0
        proof = mk_merkle_proof(header, hashes, index)

        tx = int(hashes[index], 16)
        siblings = map(partial(int,base=16), proof['siblings'])
        nSibling = len(siblings)
        path = indexToPath(index, nSibling)
        merkle = self.c.computeMerkle(tx, len(siblings), siblings, path)
        merkle %= 2 ** 256
        assert merkle == int(proof['header']['merkle_root'], 16)



    @pytest.mark.skipif(True,reason='skip')
    def testToPath(self):
        assert indexToPath(0, 2) == [2,2]
        assert indexToPath(1, 2) == [1,2]
        assert indexToPath(2, 2) == [2,1]
        assert indexToPath(3, 2) == [1,1]



    #
    # old tests, eg called storeRawBlockHeader() instead of passing binary to storeBlockHeader()
    #

    # this fails and shows that the correct way to set things up is:
    # 1. call testingonlySetGenesis() first
    # 2. call storeRawBlockHeader() of blocks AFTER the genesis
    # the correct way is done in testRandomTxVerify()
    @pytest.mark.skipif(True,reason='skip')
    def testBadSetupTxVerify(self):
        headers = [
            "01000000d153ecc827a531652c430d8895b07f6896091967d21079630321000000000000907a54a1d714ac57d8c43c8cc5b57006032fc3a5de6d97943a1e8a552fd90e11b3211b4d4c86041bb28803e8",
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        for i in range(8):  # different from testRandomTxVerify()
            res = self.c.storeRawBlockHeader(headers[i])
            assert res == i+1

        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev) # even changing this to testingonlySetHeaviest doesn't make test pass

        res = self.randomTxVerify(100000)
        assert res == 1


    # was used to find merkle_prove issue in pybitcointools
    @pytest.mark.skipif(True,reason='skip')
    def testIndexOutOfRange(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        for i in range(7):
            res = self.c.storeRawBlockHeader(headers[i])
            assert res == i+2

        res = self.randomTxVerify(100001, 8)
        assert res == 0
