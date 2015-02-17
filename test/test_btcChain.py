from pyethereum import tester
from datetime import datetime, date
import math

import pytest
slow = pytest.mark.slow

class TestBtcTx(object):

    CONTRACT = 'btcrelay.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    ANC_DEPTHS = [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536]


    def setup_class(cls):
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed

    @slow
    def testAroundMoreDepths(self):
        heaviest = 260


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)


        forkStartBlock = 999000
        parentOfFork = 2
        numBlocksInFork = 3
        for i in range(numBlocksInFork):
            self.c.saveAncestors(forkStartBlock+i, parentOfFork)
            parentOfFork = forkStartBlock


        finalAncIndex = int(math.ceil(math.log(heaviest) / math.log(4))) # log base 4 of heaviest
        # start at 1, instead of 0
        for i in range(1, finalAncIndex):
            depth = self.ANC_DEPTHS[i]
            print('@@@@@@@@@@@@@@@@@@@ depth: '+str(depth))
            assert self.c.inMainChain(depth-1) == 1
            assert self.c.inMainChain(depth) == 1
            assert self.c.inMainChain(depth+1) == 1

        for i in range(numBlocksInFork):
            assert self.c.inMainChain(forkStartBlock+i) == 0


    def testAroundSomeDepths(self):
        heaviest = 20


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)


        forkStartBlock = 999000
        parentOfFork = 2
        numBlocksInFork = 3
        for i in range(numBlocksInFork):
            self.c.saveAncestors(forkStartBlock+i, parentOfFork)
            parentOfFork = forkStartBlock


        finalAncIndex = int(math.ceil(math.log(heaviest) / math.log(4))) # log base 4 of heaviest
        # start at 1, instead of 0
        for i in range(1, finalAncIndex):
            depth = self.ANC_DEPTHS[i]
            # print('@@@@@@@@@@@@@@@@@@@ depth: '+str(depth))
            assert self.c.inMainChain(depth-1) == 1
            assert self.c.inMainChain(depth) == 1
            assert self.c.inMainChain(depth+1) == 1

        for i in range(numBlocksInFork):
            assert self.c.inMainChain(forkStartBlock+i) == 0

    def testTiny(self):

        self.c.saveAncestors(1, 0)
        self.c.saveAncestors(2, 1)
        self.c.testingonlySetHeaviest(2)

        assert self.c.inMainChain(1) == 1
        assert self.c.inMainChain(2) == 1

    def testNonExistingBlock(self):

        self.c.saveAncestors(1, 0)
        self.c.saveAncestors(2, 1)
        self.c.testingonlySetHeaviest(2)

        assert self.c.inMainChain(9876) == 0

    @pytest.mark.skipif(True,reason='skip')
    def testPerfOfStore(self):
        heaviest = 260


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)

        self.c.logAnc(heaviest)


    def testSmallChain(self):
        heaviest = 5


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)

        forkStartBlock = 999000
        parentOfFork = 2
        numBlocksInFork = 3
        for i in range(numBlocksInFork):
            self.c.saveAncestors(forkStartBlock+i, parentOfFork)
            parentOfFork = forkStartBlock

        for i in range(1, heaviest+1):
            assert self.c.inMainChain(i) == 1

        for i in range(numBlocksInFork):
            assert self.c.inMainChain(forkStartBlock+i) == 0


    def testShortFork(self):
        heaviest = 5


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)

        self.c.saveAncestors(30, 2)
        self.c.saveAncestors(31, 30)
        self.c.saveAncestors(32, 31)

        for i in range(1, heaviest+1):
            assert self.c.inMainChain(i) == 1

        assert self.c.inMainChain(30) == 0
        assert self.c.inMainChain(31) == 0
        assert self.c.inMainChain(32) == 0

        # for i in range(1, heaviest+1):
        #     self.c.logAnc(i)

        # # self.c.logAnc(63)
        # # self.c.logAnc(64)
        # # self.c.logAnc(65)
        # # self.c.logAnc(66)
        #
        # self.c.logBlockchainHead()


    # heaviest is the "fork"
    def testAltShortFork(self):
        heaviest = 5


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)

        self.c.saveAncestors(30, 2)
        self.c.saveAncestors(31, 30)
        self.c.saveAncestors(32, 31)

        self.c.testingonlySetHeaviest(32)

        for i in range(3, heaviest+1):
            assert self.c.inMainChain(i) == 0

        assert self.c.inMainChain(30) == 1
        assert self.c.inMainChain(31) == 1
        assert self.c.inMainChain(32) == 1



    # 2 forks from block2
    def testMultiShortFork(self):
        heaviest = 5


        for i in range(1, heaviest+1):
            self.c.saveAncestors(i, i-1)

        # first fork
        self.c.saveAncestors(30, 2)
        self.c.saveAncestors(31, 30)
        self.c.saveAncestors(32, 31)

        # second fork
        self.c.saveAncestors(300, 2)
        self.c.saveAncestors(310, 300)
        self.c.saveAncestors(320, 310)

        self.c.testingonlySetHeaviest(heaviest)
        for i in range(1, heaviest+1):
            assert self.c.inMainChain(i) == 1

        assert self.c.inMainChain(30) == 0
        assert self.c.inMainChain(31) == 0
        assert self.c.inMainChain(32) == 0

        assert self.c.inMainChain(300) == 0
        assert self.c.inMainChain(310) == 0
        assert self.c.inMainChain(320) == 0



        self.c.testingonlySetHeaviest(32)
        for i in range(3, heaviest+1):
            assert self.c.inMainChain(i) == 0

        assert self.c.inMainChain(30) == 1
        assert self.c.inMainChain(31) == 1
        assert self.c.inMainChain(32) == 1

        assert self.c.inMainChain(300) == 0
        assert self.c.inMainChain(310) == 0
        assert self.c.inMainChain(320) == 0


        self.c.testingonlySetHeaviest(320)
        for i in range(3, heaviest+1):
            assert self.c.inMainChain(i) == 0

        assert self.c.inMainChain(30) == 0
        assert self.c.inMainChain(31) == 0
        assert self.c.inMainChain(32) == 0

        assert self.c.inMainChain(300) == 1
        assert self.c.inMainChain(310) == 1
        assert self.c.inMainChain(320) == 1
