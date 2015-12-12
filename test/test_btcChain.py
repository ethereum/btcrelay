from ethereum import tester
from datetime import datetime, date
import math

import pytest
slow = pytest.mark.slow

from utilRelay import dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestBtcChain(object):
    CONTRACT_DEBUG = 'test/btcChain_debug.se'

    ETHER = 10 ** 18

    ANC_DEPTHS = [1, 4, 16, 64, 256, 1024, 4096, 16384]


    def setup_class(cls):
        tester.gas_limit = int(3.4e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed

    @slow
    def testAroundMoreDepths(self):
        heaviest = 260


        for i in range(1, heaviest+1):
            self.c.funcSaveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)


        forkStartBlock = 999000
        parentOfFork = 2
        numBlocksInFork = 3
        for i in range(numBlocksInFork):
            self.c.funcSaveAncestors(forkStartBlock+i, parentOfFork)
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
            self.c.funcSaveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)


        forkStartBlock = 999000
        parentOfFork = 2
        numBlocksInFork = 3
        for i in range(numBlocksInFork):
            self.c.funcSaveAncestors(forkStartBlock+i, parentOfFork)
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

        for i in range(1, heaviest+1):
            assert self.c.getBlockHash(i) == i

    def testTiny(self):

        self.c.funcSaveAncestors(1, 0)
        self.c.funcSaveAncestors(2, 1)
        self.c.testingonlySetHeaviest(2)

        assert self.c.inMainChain(1) == 1
        assert self.c.inMainChain(2) == 1

    def testNonExistingBlock(self):

        self.c.funcSaveAncestors(1, 0)
        self.c.funcSaveAncestors(2, 1)
        self.c.testingonlySetHeaviest(2)

        assert self.c.inMainChain(9876) == 0
        assert self.c.inMainChain(-1) == 0

        assert self.c.getBlockHash(9876) == 0
        assert self.c.getBlockHash(0) == 0
        assert self.c.getBlockHash(-1) == 0

    @slow
    def testPerfOfStore(self):
        heaviest = 2020

        for i in range(1, heaviest+1):
            self.c.funcSaveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)

        # self.c.logAnc(heaviest)

        for i in range(1, heaviest+1):
            assert self.c.getBlockHash(i) == i


    def testSmallChain(self):
        heaviest = 5


        for i in range(1, heaviest+1):
            self.c.funcSaveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)

        forkStartBlock = 999000
        parentOfFork = 2
        numBlocksInFork = 3
        for i in range(numBlocksInFork):
            self.c.funcSaveAncestors(forkStartBlock+i, parentOfFork)
            parentOfFork = forkStartBlock

        for i in range(1, heaviest+1):
            assert self.c.inMainChain(i) == 1

        for i in range(numBlocksInFork):
            assert self.c.inMainChain(forkStartBlock+i) == 0


    def testShortFork(self):
        heaviest = 5


        for i in range(1, heaviest+1):
            self.c.funcSaveAncestors(i, i-1)
        self.c.testingonlySetHeaviest(heaviest)

        self.c.funcSaveAncestors(30, 2)
        self.c.funcSaveAncestors(31, 30)
        self.c.funcSaveAncestors(32, 31)

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
            self.c.funcSaveAncestors(i, i-1)

        self.c.funcSaveAncestors(30, 2)
        self.c.funcSaveAncestors(31, 30)
        self.c.funcSaveAncestors(32, 31)

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
            self.c.funcSaveAncestors(i, i-1)

        # first fork
        self.c.funcSaveAncestors(30, 2)
        self.c.funcSaveAncestors(31, 30)
        self.c.funcSaveAncestors(32, 31)

        # second fork
        self.c.funcSaveAncestors(300, 2)
        self.c.funcSaveAncestors(310, 300)
        self.c.funcSaveAncestors(320, 310)

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
