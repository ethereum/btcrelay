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

    ERR_DIFFICULTY = 10010
    ERR_RETARGET = 10020

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


    @slow
    # test storing blocks right from Satoshi's genesis and past the very first
    # difficulty adjustment (the difficulty remained the same)
    # The advantage of this test is it does not fudge 'startBlock', the 2nd
    # param to setInitialParent().  Other tests below fudge the 2nd param
    # to be 0 so that the m_fastGetBlockHash() in
    # https://github.com/ethereum/btcrelay/blob/master/btcrelay.se#L116
    # will not access out of bounds.
    # A weakness of this test is that the difficulty did not change (it
    # only "changed" around 30K blocks later in testDifficultyRoundedSame() below)
    def testSameDifficulty(self):
        startBlock = 0
        self.c.setInitialParent(0, startBlock, 1)

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
    def testDifficultyAdjust(self):
        # difficulty change at 344736 was chosen since the data is contained in
        # blockchain_headers and it is a recent difficulty increase, with large
        # difficulties and the magnitude is reasonable 5%:
        # 46684376316 / 44455415962.0 = 1.050139230637394
        prevBlockHash = 0x000000000000000005d1e9e192a43a19e2fbd933ffb27df2623187ad5ce10adc
        startBlock = 342720
        self.c.setInitialParent(prevBlockHash, startBlock-1, 1)

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == startBlock-1+count

        assert self.c.getLastBlockHeight() == startBlock-1+count

        assert self.c.getCumulativeDifficulty() == \
            self.DIFF_ADJUST*44455415962 + \
            (count-self.DIFF_ADJUST)*46684376316 + 1  # score starts at 1


    # difficulty should be same when not in a block divisible by 2016
    def testDifficultyShouldBeSame(self):
        prevBlockHash = 0x000000000000000005d1e9e192a43a19e2fbd933ffb27df2623187ad5ce10adc
        startBlock = 342720
        self.c.setInitialParent(prevBlockHash, startBlock-1, 1)

        count = 3
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == startBlock-1+count

        assert self.c.getLastBlockHeight() == startBlock-1+count
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

        eventArr = []
        self.s.block.log_listeners.append(lambda x: eventArr.append(self.c._translator.listen(x)))

        res = self.c.storeBlockHeader(bhBytes)
        assert res == self.ERR_DIFFICULTY

        assert eventArr == [{'_event_type': 'Failure',
            'errCode': self.ERR_DIFFICULTY
            }]
        eventArr.pop()


    @slow
    # difficulty should match the computed new difficulty ie bits should equal newBits
    def testNewDifficultyMatch(self):
        prevBlockHash = 0x000000000000000005d1e9e192a43a19e2fbd933ffb27df2623187ad5ce10adc
        startBlock = 342720
        self.c.setInitialParent(prevBlockHash, startBlock-1, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2016
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == startBlock-1+count

        assert self.c.getLastBlockHeight() == startBlock-1+count
        assert self.c.getCumulativeDifficulty() == count*44455415962 + 1  # score starts at 1

        # adding a low difficulty block should fail since bits!=newBits
        version = 2
        hashMerkleRoot = 0 # doesn't matter
        time = 1424648937  # same as real block 344736
        bits = 0x207FFFFF  # REGTEST_EASIEST_DIFFICULTY
        nonce = 0
        hashPrevBlock = 0x00000000000000000f9e30784bd647e91f6923263a674c9c5c18084fe79a41f8  # block 344735
        bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        assert dblSha256Flip(bhBytes) == 0x0016127022e6debe87071eb0091918d2fccbcef0d46a046bcaf71309b0528044
        assert self.c.getBlockchainHead() == hashPrevBlock

        eventArr = []
        self.s.block.log_listeners.append(lambda x: eventArr.append(self.c._translator.listen(x)))

        res = self.c.storeBlockHeader(bhBytes)
        assert res == self.ERR_RETARGET

        assert eventArr == [{'_event_type': 'Failure',
            'errCode': self.ERR_RETARGET
            }]
        eventArr.pop()

        # add the real block
        version = 2
        hashMerkleRoot = 0x734c8b7ea7767005409c23a4b907d07329dadc4bac573b2c809f642eec4de26b
        time = 1424648937
        bits = 404196666
        nonce = 550403378
        hashPrevBlock = 0x00000000000000000f9e30784bd647e91f6923263a674c9c5c18084fe79a41f8  # block 344735
        bhBytes = getHeaderBytes(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
        assert dblSha256Flip(bhBytes) == 0x00000000000000001097f043cca218169e00623c9962b25a0b159eaca2d8ca25
        assert self.c.getBlockchainHead() == hashPrevBlock
        assert self.c.storeBlockHeader(bhBytes) == startBlock-1+count + 1
        assert count + 1 == 2017


    @slow
    def testDecreaseDifficulty(self):
        # big difficulty decrease March 25 2011 block number 127008
        prevBlockHash = 0x00000000000033e435c4bbddc7eb255146aa7f18e61a832983af3a9ee5dd144d
        startBlock = 124992
        self.c.setInitialParent(prevBlockHash, startBlock-1, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == startBlock-1+count

        assert self.c.getLastBlockHeight() == startBlock-1+count

        assert self.c.getCumulativeDifficulty() == \
            self.DIFF_ADJUST*244112 + \
            (count-self.DIFF_ADJUST)*434877 + 1  # score starts at 1


    @slow
    # The difficulty changed from 1.0 to 1.18, but the same since it's rounded
    # http://bitcoin.stackexchange.com/questions/22581/how-was-the-new-target-for-block-32256-calculated
    def testDifficultyRoundedSame(self):
        prevBlockHash = 0x000000005107662c86452e7365f32f8ffdc70d8d87aa6f78630a79f7d77fbfe6
        startBlock = 30240
        self.c.setInitialParent(prevBlockHash, startBlock-1, 1)  # start at 0, for difficultyAdjustment tests otherwise getBlockHash out of bounds

        count = 2020
        with open("test/headers/blockchain_headers") as f:
            f.seek(80 * startBlock)
            bhBytes = f.read(80 * count)
            assert self.c.bulkStoreHeader(bhBytes, count) == startBlock-1+count

        assert self.c.getLastBlockHeight() == startBlock-1+count

        assert self.c.getCumulativeDifficulty() == \
            self.DIFF_ADJUST*1 + \
            (count-self.DIFF_ADJUST)*1 + 1  # score starts at 1


    # based on https://github.com/petertodd/python-bitcoinlib/blob/2a5dda45b557515fb12a0a18e5dd48d2f5cd13c2/bitcoin/tests/test_serialize.py#L131
    def testToCompactBits(self):
        assert self.c.funcToCompactBits(0x1234) == 0x02123400
        assert self.c.funcToCompactBits(0x123456) == 0x03123456
        assert self.c.funcToCompactBits(0x12345600) == 0x04123456
        assert self.c.funcToCompactBits(0x92340000) == 0x05009234
        assert self.c.funcToCompactBits(0x1234560000000000000000000000000000000000000000000000000000000000) == 0x20123456
