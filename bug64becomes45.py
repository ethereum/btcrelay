
data block[2^256](_height, _ancestor[], _blockHeader(_prevBlock))

data numAncestorDepths
def initAncestorDepths():
    self.numAncestorDepths = 2

def testStoreB(number, blockHash, hashPrevBlock):
    self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock
    self.block[blockHash]._height = number

    log(self.numAncestorDepths)


def test2():
    self.initAncestorDepths()
    self.testStoreB(45, 45, 44)
    self.testStoreB(46, 46, 45)
