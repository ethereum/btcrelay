from pyethereum import tester
from datetime import datetime, date

import pytest
slow = pytest.mark.slow

class TestBtcBulkStoreHeaders(object):

    CONTRACT = 'btcBulkStoreHeaders.py'
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
    # @pytest.mark.veryslow
    def testBSH(self):
        startBlockNum = 300000
        numBlock = 60

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        nLoop = 2
        i = 1
        j = 0

        while j < nLoop:
            strings = ""
            with open("test/headers/500from300k.txt") as f:
                for header in f:
                    strings += header[:-1]
                    if i==numBlock:
                        break
                    i += 1

            headerBins = strings.decode('hex')  # [:-1] to remove trailing \n
            res = self.c.bulkStoreHeader(headerBins, numBlock)

            assert res == 1 + (numBlock * (j+1))

            j += 1


        # startTime = datetime.now().time()
        # endTime = datetime.now().time()
        #
        # duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        # print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        # assert res == 1 + numBlock


    def testBulkStore7(self):
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

        count = 7
        strings = ""
        for i in range(count):
            strings += headers[i]

        headerBins = strings.decode('hex')

        res = self.c.bulkStoreHeader(headerBins, count)
        assert res == 1 + count


    @slow
    # @pytest.mark.veryslow
    def testBulkStore60(self):
        startBlockNum = 300000
        numBlock = 60

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        strings = ""
        i = 1
        with open("test/headers/500from300k.txt") as f:
            for header in f:
                strings += header[:-1]
                if i==numBlock:
                    break
                i += 1

        headerBins = strings.decode('hex')  # [:-1] to remove trailing \n

        startTime = datetime.now().time()
        res = self.c.bulkStoreHeader(headerBins, numBlock)
        endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        assert res == 1 + numBlock
