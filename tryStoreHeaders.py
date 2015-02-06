
data numAncestorDepths
self.numAncestorDepths = 9  # if change, look at defn of ancestor_depths and block structures
data ancestor_depths[9]
# note: _ancestor[9]
data block[2^256](_height, _score, _ancestor[9], _blockHeader(_version, _prevBlock, _mrklRoot, _time, _bits, _nonce))


data heaviestBlock

# highest score among all blocks (so far)
data highScore




def testStoreB(number, blockHash, hashPrevBlock):
    self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock
    self.block[blockHash]._height = number

    i = 0
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]
        self.block[blockHash]._ancestor[i] = self.block[blockHash]._height - depth

        # log(3333333333333)
        # log(self.block[blockHash]._ancestor[i])

        # log(3333333333333)
        # log(depth)
        # log(blockHash * 1000000)
        # log(self.block[blockHash]._height % depth)
        # if self.block[blockHash]._height % depth == 1:
        #     log(444444444)
        #     log(hashPrevBlock)
        #     # log(self.block[blockHash]._height)
        #     # log(depth)
        #     self.block[blockHash]._ancestor[i] = hashPrevBlock
        # else:
        #     # log(77777777777)
        #     self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i] # or i-1?

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

# in chain:
#     b = head
#     anc_index = ancestor_count - 1
#     while b.number > block.number:
#         while b.number - block.number < ancestor_depths[anc_index] and anc_index > 0:
#             anc_index -= 1
#         b = b.ancestors[anc_index]
#     return b == block

def inMainChain(txBlockHash):
    blockHash = self.heaviestBlock

    anc_index = self.numAncestorDepths - 1
    while self.block[blockHash]._height > txBlockHash:
        while self.block[blockHash]._height - txBlockHash < self.ancestor_depths[anc_index] && anc_index > 0:
            anc_index -= 1
        blockHash = self.block[blockHash]._ancestor[anc_index]

    return(blockHash == txBlockHash)


def logAnc(blockHash):
    log(11111)
    log(blockHash)
    i = 0
    while i < self.numAncestorDepths:
        anc = self.block[blockHash]._ancestor[i]
        log(anc)
        i += 1
    log(22222)

def testSetHeaviest(blockHash):
    self.heaviestBlock = blockHash


def initAncestorDepths():
    i = 0
    while i < self.numAncestorDepths:
        self.ancestor_depths[i] = 4 ^ i
        log(self.ancestor_depths[i])
        i += 1


def logBlockchainHead():
    log(self.heaviestBlock)
