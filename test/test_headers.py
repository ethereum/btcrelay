from pyethereum import tester
from datetime import datetime, date
from functools import partial

from bitcoin import *

import math

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


    def randomTx(self, blocknum):
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

    def test100from300K(self):
        startBlockNum = 300000
        numBlock = 10

        i = 1
        with open("test/headers/100from300k.txt") as f:
            for header in f:
                res = self.c.storeRawBlockHeader(header)
                if i==numBlock:
                    break
                assert res == i
                i += 1

        block300k = 0x000000000000000082ccf8f1557c5d40b21edabb18d2d691cfbf87118bac7254
        self.c.testingonlySetGenesis(block300k)
        for i in range(5):
            randBlock = random.randrange(startBlockNum, startBlockNum+numBlock)
            self.randomTx(randBlock)



    def testRandomTx(self):
        self.randomTx(100000)


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
