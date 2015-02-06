
data block[2^256](_blockHeader(_prevBlock))

data numAncestorDepths
def initAncestorDepths():
    self.numAncestorDepths = 2

def testStoreB(number, blockHash, hashPrevBlock):
    self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock

    log(self.numAncestorDepths)


def test2():
    self.initAncestorDepths()
    self.testStoreB(45, 45, 44)
    self.testStoreB(46, 46, 45)  # this will log 45 (expected is to still log 2)
