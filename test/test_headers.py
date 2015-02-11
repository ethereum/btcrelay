from pyethereum import tester
from datetime import datetime, date
from functools import partial

from bitcoin import *

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


    def testProof(self):
        blocknum = 100000
        header = get_block_header_data(blocknum)
        hashes = get_txs_in_block(blocknum)
        index = 0
        proof = mk_merkle_proof(header, hashes, index)

        tx = int(hashes[index], 16)
        siblings = map(partial(int,base=16), proof['siblings'])
        merkle = self.c.computeMerkle(tx, len(siblings), siblings, [2, 2])
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
