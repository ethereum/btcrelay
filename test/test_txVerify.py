from pyethereum import tester
from datetime import datetime, date
from functools import partial

from bitcoin import *

import math
import time

import pytest
slow = pytest.mark.slow

class TestBtcTx(object):

    CONTRACT = 'btcTx.py'
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
    def randomTxVerify(self, blocknum, txIndex=-1):
        header = get_block_header_data(blocknum)
        hashes = get_txs_in_block(blocknum)

        numTx = len(hashes)
        if numTx == 0:
            print('@@@@ empty blocknum='+str(blocknum))
            return

        index = random.randrange(numTx) if txIndex == -1 else txIndex

        print('txStr='+hashes[index])

        proof = mk_merkle_proof(header, hashes, index)

        print('@@@@@@@@@@@@@@@@ blocknum='+str(blocknum)+'\ttxIndex='+str(index))

        tx = int(hashes[index], 16)
        siblings = map(partial(int,base=16), proof['siblings'])
        nSibling = len(siblings)
        path = self.indexToPath(index, nSibling)
        txBlockHash = int(header['hash'], 16)
        res = self.c.verifyTx(tx, len(siblings), siblings, path, txBlockHash)
        return res


    @pytest.mark.skipif(True,reason='skip')
    def test80from300K(self):
        startBlockNum = 300000
        numBlock = 80

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        i = 1
        with open("test/headers/100from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeRawBlockHeader(header)
                if i==numBlock:
                    break
                i += 1
                assert res == i

            endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))


    @pytest.mark.skipif(True,reason='skip')
    def test100from300K(self):
        startBlockNum = 300000
        numBlock = 400

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        i = 1
        with open("test/headers/500from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeRawBlockHeader(header)
                if i==numBlock:
                    break
                i += 1
                assert res == i

            endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        nChecks = 400000
        for i in range(nChecks):
            if i > 20:
                time.sleep(1)
            if i%60 == 0:
                print(i)

            randBlock = random.randrange(startBlockNum, startBlockNum+numBlock)
            res = self.randomTxVerify(randBlock)

            # should only verify when more than 6 confirmations
            if randBlock < startBlockNum+numBlock-6:
                assert res == 1
            else:
                assert res == 0


    # this was fine, the assertion was wrong, so need to carefully check the assert
    @pytest.mark.skipif(True,reason='skip')
    def test17index2(self):
        startBlockNum = 300000
        numBlock = 30

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.testingonlySetGenesis(block300kPrev)

        i = 1
        with open("test/headers/100from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeRawBlockHeader(header)
                if i==numBlock:
                    break
                i += 1
                assert res == i

            endTime = datetime.now().time()

        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))

        res = self.randomTxVerify(300017, 2)
        # assert res == 0  # adjust according to numBlock

    # this fails and shows that the correct way to set things up is:
    # 1. call testingonlySetGenesis() first
    # 2. call storeRawBlockHeader() of blocks AFTER the genesis
    # the correct was is done in testRandomTxVerify()
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
            res = self.c.storeRawBlockHeader(headers[i], blockHeaderBinary[i])
            assert res == i+2

        startBlockNum = 100000
        numBlock = 7
        for i in range(startBlockNum, startBlockNum+numBlock):
            res = self.randomTxVerify(i)
            if i < startBlockNum+numBlock-6:
                assert res == 1
            else:
                assert res == 0

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
        path = self.indexToPath(index, nSibling)
        merkle = self.c.computeMerkle(tx, len(siblings), siblings, path)
        merkle %= 2 ** 256
        assert merkle == int(proof['header']['merkle_root'], 16)

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
        path = self.indexToPath(index, nSibling)
        merkle = self.c.computeMerkle(tx, len(siblings), siblings, path)
        merkle %= 2 ** 256
        assert merkle == int(proof['header']['merkle_root'], 16)



    @slow
    @pytest.mark.skipif(True,reason='skip')
    def testSB(self):
        print("jstart")
        i = 1
        with open("test/headers/bh80k.txt") as f:
            startTime = datetime.now().time()

            for header in f:
                # print(header)
                res = self.c.storeRawBlockHeader(header)
                if i==20:
                    break
                assert res == [i]
                i += 1

            endTime = datetime.now().time()

        # with open("test/headers/bh80_100k.txt") as f:
        #     for header in f:
        #         # print(header)
        #         res = self.c.storeRawBlockHeader(header)
        #         assert res == [i]
        #         i += 1
        #
        # with open("test/headers/bh100_150k.txt") as f:
        #     for header in f:
        #         # print(header)
        #         res = self.c.storeRawBlockHeader(header)
        #         assert res == [i]
        #         i += 1


        self.c.logBlockchainHead()

        print "gas used: ", self.s.block.gas_used
        duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))
        print("jend")

        # h = "0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c"
        # res = self.c.storeRawBlockHeader(h)
        # assert res == [1]



    @pytest.mark.skipif(True,reason='skip')
    def testToPath(self):
        assert self.indexToPath(0, 2) == [2,2]
        assert self.indexToPath(1, 2) == [1,2]
        assert self.indexToPath(2, 2) == [2,1]
        assert self.indexToPath(3, 2) == [1,1]


    # for now, read the bits of n in order (from least significant)
    # and convert 0 -> 2 and 1 -> 1
    def indexToPath(self, n, nSibling):
        ret = []
        if n == 0:
            ret = [2] * nSibling
        else:
            bits = int(math.log(n, 2)+1)
            for i in range(bits):
                if self.checkBit(n, i) == 0:
                    ret.append(2)
                else:
                    ret.append(1)

            if bits < nSibling:
                ret = ret + ([2] * (nSibling - bits))
        return ret


    def checkBit(self, int_type, offset):
        mask = 1 << offset
        return(int_type & mask)
