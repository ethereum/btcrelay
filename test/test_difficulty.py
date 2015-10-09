from ethereum import tester

import datetime
import struct
import pytest
slow = pytest.mark.slow

from utilRelay import getHeaderBytes, dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestDifficulty(object):

    # very specialized test
    CONTRACT_DEBUG = 'test/btcrelay_difficulty.se'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(2.85e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def testComputeNewBits(self):
        prevTime = 1443699609  # block 376991
        startTime = 1442519404 # block 374976
        prevBits = 403867578
        prevTarget = self.c.funcTargetFromBits(prevBits)
        expBits = 403838066
        assert self.c.funcComputeNewBits(prevTime, startTime, prevTarget) == expBits

        # http://bitcoin.stackexchange.com/questions/22581/how-was-the-new-target-for-block-32256-calculated
        prevTime = 1262152739
        startTime = 1261130161
        prevBits = 0x1d00ffff
        prevTarget = self.c.funcTargetFromBits(prevBits)
        expBits = 0x1d00d86a
        assert self.c.funcComputeNewBits(prevTime, startTime, prevTarget) == expBits

        # big difficulty decrease March 25 2011 block number 127008
        prevTime = 1306435280
        startTime = 1305756287
        prevBits = 440711666
        prevTarget = self.c.funcTargetFromBits(prevBits)
        expBits = 438735905
        assert self.c.funcComputeNewBits(prevTime, startTime, prevTarget) == expBits


    def tmp2(self):
        # block100002 with all real data (hashes, time) except fake 'bits' and nonce
        version = 1
        hashPrevBlock = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090  # block100001
        hashMerkleRoot = 0x2fda58e5959b0ee53c5253da9b9f3c0c739422ae04946966991cf55895287552
        time = 1293625051
        bits = 0x207fFFFFL # REGTEST_EASIEST_DIFFICULTY
        nonce = 2
        bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)

        currTime = self.c.funcTimestampViaCALLDATALOAD(bhBytes)
        assert currTime == time

        # block100k (100002 - DIFFICULTY_ADJUSTMENT_INTERVAL)
        startTime = 1293623863
        currTarget = 0x000000000004864c000000000000000000000000000000000000000000000000

        newTarget = self.c.funcComputeNewTarget(currTime, startTime, currTarget)
        assert newTarget == 123


    def tmp(self):
        # block 100001
        header = '0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b'
        expTime = 1293624404


    # TODO needed?
    def testTimestampFromCurrentBlockHeader(self):
        # block100K
        header = '0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710'
        expTime = 1293623863
        assert self.c.funcTimestampViaCALLDATALOAD(header.decode('hex')) == expTime


    def testDifficultyAdjust(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        blockPrevNum = 1  # for this special test
        self.c.setInitialParent(block100kPrev, blockPrevNum, 1)

        # TODO repeat this test but with 1 header, and then 7 headers?
        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b"
            #"0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(len(headers)):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])

            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+1+blockPrevNum

        cumulDiff = self.c.getCumulativeDifficulty()

        height = self.c.getLastBlockHeight()
        print 'height: ' + str(height)


        # insert block with lower difficulty
        # using script/mine.py (commit 3908709) this block
        # nonce: 2 blockhash: 72bb4c2a6781d464fb42c4aea95c5cafa7430ff026170d6a2c92e9a5c26f0fbe
        REGTEST_EASIEST_DIFFICULTY = 0x207fFFFFL
        version = 1
        # real merkle of block100001
        hashMerkleRoot = 0x7fe79307aeb300d910d9c4bec5bacb4c7e114c7dfd6789e19f3a733debb3bb6a
        time = 1293625051  # from block100k
        bits = REGTEST_EASIEST_DIFFICULTY
        nonce = 0
        hashPrevBlock = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090  # block100001
        bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        res = self.c.storeBlockHeader(bhBytes)
        # assert res == 100002
        assert res == 77
