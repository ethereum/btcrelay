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
    DIFF_ADJUST = 2016

    def setup_class(cls):
        tester.gas_limit = int(500e6)  # include costs of debug methods
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
        prevTime = 1262152739  # 32255
        startTime = 1261130161  # 30240
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

        # mock uses REGTEST_EASIEST_DIFFICULTY and tests the boundary of
        # retargeting to DIFFICULTY_1 which is 0x1d00ffff
        prevTime = 1443699609  # block 376991
        startTime = 1442519404 # block 374976
        prevBits = 0x207FFFFF  # REGTEST_EASIEST_DIFFICULTY
        prevTarget = self.c.funcTargetFromBits(prevBits)
        expBits = 0x1d00ffff
        assert self.c.funcComputeNewBits(prevTime, startTime, prevTarget) == expBits


    # TODO needed?
    def testTimestampFromCurrentBlockHeader(self):
        # block100K
        header = '0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710'
        expTime = 1293623863
        assert self.c.funcTimestampViaCALLDATALOAD(header.decode('hex')) == expTime


    @slow
    def testDifficultyAdjust(self):
        # difficulty change at 344736 was chosen since the data is contained in
        # blockchain_headers and it is a recent difficulty increase, with large
        # difficulties and the magnitude is reasonable 5%:
        # 46684376316 / 44455415962.0 = 1.050139230637394
        prevBlockHash = 0x000000000000000005d1e9e192a43a19e2fbd933ffb27df2623187ad5ce10adc
        startBlock = 342720
        self.c.setInitialParent(prevBlockHash, 0, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == count

        assert self.c.getLastBlockHeight() == count

        assert self.c.getCumulativeDifficulty() == \
            self.DIFF_ADJUST*44455415962 + \
            (count-self.DIFF_ADJUST)*46684376316 + 1  # score starts at 1


    # difficulty should be same when not in a block divisible by 2016
    def testDifficultyShouldBeSame(self):
        prevBlockHash = 0x000000000000000005d1e9e192a43a19e2fbd933ffb27df2623187ad5ce10adc
        startBlock = 342720
        self.c.setInitialParent(prevBlockHash, 0, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 3
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == count

        assert self.c.getLastBlockHeight() == count
        assert self.c.getCumulativeDifficulty() == count*44455415962 + 1  # score starts at 1

        # adding a low difficulty block should fail since bits!=prevBits
        version = 1
        hashMerkleRoot = 0 # doesn't matter
        time = 1423499049  # same as real block 342723
        bits = 0x207FFFFF  # REGTEST_EASIEST_DIFFICULTY
        nonce = 0
        hashPrevBlock = 0x000000000000000004db26747ccd2feb6341c18282a33e2c5d8eb84a1b12d951  # block 342722
        bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        assert dblSha256Flip(bhBytes) == 0x2afa6cec2435698406ff2138ae6162469857524c7849970e5bb82039e90a099b
        res = self.c.storeBlockHeader(bhBytes)
        assert res == 99


    # difficulty should match the computed new difficulty ie bits should equal newBits
    def testNewDifficultyMatch(self):
        prevBlockHash = 0x000000000000000005d1e9e192a43a19e2fbd933ffb27df2623187ad5ce10adc
        startBlock = 342720
        self.c.setInitialParent(prevBlockHash, 0, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2015
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == count

        assert self.c.getLastBlockHeight() == count
        assert self.c.getCumulativeDifficulty() == count*44455415962 + 1  # score starts at 1

        # adding a low difficulty block should fail since bits!=newBits
        # version = 2
        # hashMerkleRoot = 0 # doesn't matter
        # time = 1424648937  # same as real block 344736
        # bits = 0x207FFFFF  # REGTEST_EASIEST_DIFFICULTY
        # nonce = 0
        # hashPrevBlock = 0x00000000000000000f9e30784bd647e91f6923263a674c9c5c18084fe79a41f8  # block 344735
        # bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        # assert dblSha256Flip(bhBytes) == 0x0016127022e6debe87071eb0091918d2fccbcef0d46a046bcaf71309b0528044
        # res = self.c.storeBlockHeader(bhBytes)
        # assert res == 77


        # add the real block
        version = 2
        hashMerkleRoot = 0x734c8b7ea7767005409c23a4b907d07329dadc4bac573b2c809f642eec4de26b
        time = 1424648937
        bits = 404196666  # REGTEST_EASIEST_DIFFICULTY
        nonce = 550403378
        hashPrevBlock = 0x00000000000000000f9e30784bd647e91f6923263a674c9c5c18084fe79a41f8  # block 344735
        bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        assert dblSha256Flip(bhBytes) == 0x00000000000000001097f043cca218169e00623c9962b25a0b159eaca2d8ca25
        assert self.c.storeBlockHeader(bhBytes) == count + 1
        assert count + 1 == 2016


    @slow
    def testDecreaseDifficulty(self):
        # big difficulty decrease March 25 2011 block number 127008
        prevBlockHash = 0x00000000000033e435c4bbddc7eb255146aa7f18e61a832983af3a9ee5dd144d
        startBlock = 124992
        self.c.setInitialParent(prevBlockHash, 0, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == count

        assert self.c.getLastBlockHeight() == count

        assert self.c.getCumulativeDifficulty() == \
            self.DIFF_ADJUST*244112 + \
            (count-self.DIFF_ADJUST)*434877 + 1  # score starts at 1


    @slow
    # test storing blocks right from Satoshi's genesis and past the very first
    # difficulty adjustment (the difficulty remained the same)
    def testSameDifficulty(self):
        startBlock = 0
        self.c.setInitialParent(0, startBlock, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            res = self.c.bulkStoreHeader(bhBytes, count, profiling=True)
            # print('GAS: '+str(res['gas']))
            assert res['output'] == startBlock + count

        assert self.c.getLastBlockHeight() == count

        assert self.c.getCumulativeDifficulty() == count*1 + 1  # score starts at 1


    @slow
    # The difficulty changed from 1.0 to 1.18, but the same since it's rounded
    # http://bitcoin.stackexchange.com/questions/22581/how-was-the-new-target-for-block-32256-calculated
    def testDifficultyRoundedSame(self):
        prevBlockHash = 0x000000005107662c86452e7365f32f8ffdc70d8d87aa6f78630a79f7d77fbfe6
        startBlock = 30240
        self.c.setInitialParent(prevBlockHash, 0, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == count

        assert self.c.getLastBlockHeight() == count

        assert self.c.getCumulativeDifficulty() == \
            self.DIFF_ADJUST*1 + \
            (count-self.DIFF_ADJUST)*1 + 1  # score starts at 1


    def tmp3(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        blockPrevNum = 0
        self.c.setInitialParent(block100kPrev, blockPrevNum, 1)

        # TODO repeat this test but with 1 header, and then 7 headers?
        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2"
        ]
        blockHeaderBytes = map(lambda x: x.decode('hex'), headers)
        for i in range(len(headers)):
            res = self.c.storeBlockHeader(blockHeaderBytes[i])

            print 'res sb: ' + str(res)

            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+1+blockPrevNum

        assert 0

        cumulDiff = self.c.getCumulativeDifficulty()

        height = self.c.getLastBlockHeight()
        print '@@@ height: ' + str(height)

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

        # block100k (100002 - DIFF_ADJUST)
        startTime = 1293623863
        currTarget = 0x000000000004864c000000000000000000000000000000000000000000000000

        newTarget = self.c.funcComputeNewTarget(currTime, startTime, currTarget)
        assert newTarget == 123


    def tmp(self):
        # block 100001
        header = '0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b'
        expTime = 1293624404
