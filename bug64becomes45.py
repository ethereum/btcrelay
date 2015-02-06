
# data heaviestBlock

data block[2^256](_height, _ancestor[], _blockHeader(_prevBlock))

data numAncestorDepths
data ancestor_depths[8]
def initAncestorDepths():
    self.numAncestorDepths = 8
    i = 1
    while i <= self.numAncestorDepths:
        self.ancestor_depths[i - 1] = 4 ^ i
        log(self.ancestor_depths[i - 1])
        i += 1

def testStoreB(number, blockHash, hashPrevBlock):
    self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock
    self.block[blockHash]._height = number

    log(self.numAncestorDepths*1000000000000)
    i = 0
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]
        # log(3333333333333)
        log(depth)
        if self.block[blockHash]._height % depth == 1:
            self.block[blockHash]._ancestor[i] = hashPrevBlock
        else:
            self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i] # or i-1?
        i += 1
    log(self.numAncestorDepths*1000000000000)


def test2():
    self.initAncestorDepths()
    self.testStoreB(45, 45, 44)
    self.testStoreB(46, 46, 45)
