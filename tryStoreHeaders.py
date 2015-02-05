
data heaviestBlock

# highest score among all blocks (so far)
data highScore

data block[2^256](_height, _score, _ancestor[], _blockHeader(_version, _prevBlock, _mrklRoot, _time, _bits, _nonce))


def testStoreB(number, blockHash, hashPrevBlock):
    self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock
    self.block[blockHash]._height = number

    i = 0
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]
        # log(depth)
        if self.block[blockHash]._height % depth:
            # log('44')
            self.block[blockHash]._ancestor[i] = hashPrevBlock
        else:
            # log('77')
            self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i] # or i-1?
        i += 1

def logAnc(blockHash):
    i = 0
    while i < 8:
        anc = self.block[blockHash]._ancestor[i]
        log(anc)
        i += 1

def testSetHeaviest(blockHash):
    self.heaviestBlock = blockHash

data numAncestorDepths
self.numAncestorDepths = 8
data ancestor_depths[8]
def initAncestorDepths():
    i = 1
    while i <= self.numAncestorDepths:
        self.ancestor_depths[i - 1] = 4 ^ i
        i += 1


def logBlockchainHead():
    log(self.heaviestBlock)
