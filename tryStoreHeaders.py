
data numAncestorDepths
self.numAncestorDepths = 9  # if change, look at defn of ancestor_depths and block in btcrelay.py
data ancestor_depths[9]


# def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
#     # this check can be removed to allow older block headers to be added, but it
#     # may provide an attack vector where the contract can be spammed with valid
#     # headers that will not be used and simply take up memory storage
#     if hashPrevBlock != self.heaviestBlock:  # special case for genesis prev block of 0 is not needed since self.heaviestBlock is 0 initially
#         return(0)
#
#     blockHash = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
#     target = self.targetFromBits(bits)
#
#     log(target)
#
#     difficulty = DIFFICULTY_1 / target # https://en.bitcoin.it/wiki/Difficulty
#
#     # TODO other validation of block?  eg timestamp
#
#     if gt(blockHash, 0) && lt(blockHash, target):
#         self.block[blockHash]._blockHeader._version = version
#         self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock
#         self.block[blockHash]._blockHeader._mrklRoot = hashMerkleRoot
#         self.block[blockHash]._blockHeader._time = time
#         self.block[blockHash]._blockHeader._bits = bits
#         self.block[blockHash]._blockHeader._nonce = nonce
#
#         self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty
#
#
#         self.block[blockHash]._height = self.block[hashPrevBlock]._height + 1
#
#         if gt(self.block[blockHash]._score, highScore):
#             self.heaviestBlock = blockHash
#             highScore = self.block[blockHash]._score
#
#         return(self.block[blockHash]._height)
#
#     return(0)

def testStoreB(blockHash, hashPrevBlock):
    self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock

    # this is a test; separate genesis function could help later
    # if blockHash == 1:
    #     self.block[blockHash]._height = 1
    # else:
    self.block[blockHash]._height = self.block[hashPrevBlock]._height + 1

    self.block[blockHash]._ancestor[0] = hashPrevBlock
    i = 1
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]

        if self.block[blockHash]._height % depth == 1:
            self.block[blockHash]._ancestor[i] = hashPrevBlock
        else:
            self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i]
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
    txBlockHeight = self.block[txBlockHash]._height
    if !txBlockHeight:
        return(0)

    blockHash = self.heaviestBlock

    anc_index = self.numAncestorDepths - 1
    while self.block[blockHash]._height > txBlockHeight:
        while self.block[blockHash]._height - txBlockHeight < self.ancestor_depths[anc_index] && anc_index > 0:
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
