
data numAncestorDepths
self.numAncestorDepths = 8
data ancestor_depths[8]

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
        # log(3333333333333)
        # log(depth)
        # log(blockHash * 1000000)
        # log(self.block[blockHash]._height % depth)
        if self.block[blockHash]._height % depth == 1:
            # log(444444444)
            # log(self.block[blockHash]._height)
            # log(depth)
            self.block[blockHash]._ancestor[i] = hashPrevBlock
        else:
            # log(77777777777)
            self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i] # or i-1?

            # if self.block[blockHash]._ancestor[i] == 45:
                # log(88888888)
                # log(self.block[blockHash]._height)
                # log(depth)
            #     log(blockHash)
            #     log(hashPrevBlock)
            #     log(i)
            #     log(self.block[blockHash]._ancestor[i-2])
            #     log(self.block[blockHash]._ancestor[i-1])
            #     log(self.block[blockHash]._ancestor[i])

        i += 1

def logAnc(blockHash):
    log(11111)
    log(blockHash)
    i = 0
    while i < 8:
        anc = self.block[blockHash]._ancestor[i]
        log(anc)
        i += 1
    log(22222)

def testSetHeaviest(blockHash):
    self.heaviestBlock = blockHash


def initAncestorDepths():
    i = 1
    while i <= self.numAncestorDepths:
        self.ancestor_depths[i - 1] = 4 ^ i
        log(self.ancestor_depths[i - 1])
        i += 1


def logBlockchainHead():
    log(self.heaviestBlock)
