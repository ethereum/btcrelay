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


    def testBulkStore10AndRelay(self):
        startBlockNum = 300000
        numBlock = 10

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
        # print('@@@ hb: ', headerBins)

        res = self.c.bulkStoreHeader(headerBins, numBlock, profiling=True)

        print('GAS: '+str(res['gas']))
        assert res['output'] == 1 + numBlock


        # block 300000
        header =
        hashes =

        # tx[1] 7301b595279ece985f0c415e420e425451fcf7f684fcce087ba14d10ffec1121
        txStr = '01000000014dff4050dcee16672e48d755c6dd25d324492b5ea306f85a3ab23b4df26e16e9000000008c493046022100cb6dc911ef0bae0ab0e6265a45f25e081fc7ea4975517c9f848f82bc2b80a909022100e30fb6bb4fb64f414c351ed3abaed7491b8f0b1b9bcd75286036df8bfabc3ea5014104b70574006425b61867d2cbb8de7c26095fbc00ba4041b061cf75b85699cb2b449c6758741f640adffa356406632610efb267cb1efa0442c207059dd7fd652eeaffffffff020049d971020000001976a91461cf5af7bb84348df3fd695672e53c7d5b3f3db988ac30601c0c060000001976a914fd4ed114ef85d350d6d40ed3f6dc23743f8f99c488ac00000000'
        merkleProof = self.makeMerkleProof(header, hashes, 1)


        # verify the proof and then hand the proof to the btc-eth contract, which will check
        # the tx outputs and send ether as appropriate
        BTC_ETH = self.s.abi_contract('btc-eth.py', endowment=2000*self.ETHER)
        BTC_ETH.setTrustedBtcRelay(self.c.address)
        res = self.doRelayTx(txStr, merkleProof, BTC_ETH.address, profiling=True)
        assert(res == 1)

        ethAddrBin = txStr[-52:-12].decode('hex')
        userEthBalance = self.s.block.get_balance(ethAddrBin)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 13
        assert userEthBalance == expEtherBalance
        assert res == 1  # ether was transferred

        assert 0 == self.doRelayTx(txStr, merkleProof, BTC_ETH.address)  # re-claim disallowed





    @slow
    # @pytest.mark.veryslow
    def testBulkStore120(self):
        startBlockNum = 300000
        numBlock = 60

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        nLoop = 2
        j = 0
        with open("test/headers/500from300k.txt") as f:
            while j < nLoop:
                i = 1
                strings = ""
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
        # print('@@@ hb: ', headerBins)

        startTime = datetime.now().time()
        res = self.c.bulkStoreHeader(headerBins, numBlock, profiling=True)
        endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        print('GAS: '+str(res['gas']))
        assert res['output'] == 1 + numBlock




    # we generally want to skip this since it is covered by BulkStore60
    @pytest.mark.veryslow
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
