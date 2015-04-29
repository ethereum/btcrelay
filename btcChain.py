# btcChain is required by btcrelay and is a separate file to improve
# clarity: it has ancestor management and its
# main method is inMainChain() which is tested by test_btcChain

data numAncestorDepths
self.numAncestorDepths = 8  # if changing this, need to do so carefully eg look at defn of ancestor_depths and block in btcrelay
data ancestor_depths[8]

self.ancestor_depths[0] = 1
self.ancestor_depths[1] = 4
self.ancestor_depths[2] = 16
self.ancestor_depths[3] = 64
self.ancestor_depths[4] = 256
self.ancestor_depths[5] = 1024
self.ancestor_depths[6] = 4096
self.ancestor_depths[7] = 16384


# list for internal usage only that allows a 32 byte blockHash to be looked up
# with a 32bit int
# This is not designed to be used for anything else, eg it contains all block
# hashes and nothing can be assumed about which blocks are on the main chain
data internalBlock[2^50]

# counter for next available slot in internalBlock
data ibIndex


# save the ancestors for a block, as well as updating the height
def saveAncestors(blockHash, hashPrevBlock):
    self.internalBlock[self.ibIndex] = blockHash
    self.block[blockHash]._ibIndex = self.ibIndex
    self.ibIndex += 1


    self.block[blockHash]._height = self.block[hashPrevBlock]._height + 1

    # 8 indexes into internalBlock can be stored inside one ancestor (32 byte) word
    ancWord = 0

    # the first ancestor is the index to hashPrevBlock, and write it to ancWord
    prevIbIndex = self.block[hashPrevBlock]._ibIndex
    m_mstore32(ref(ancWord), prevIbIndex)

    # update ancWord with the remaining indexes
    i = 1
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]

        if self.block[blockHash]._height % depth == 1:
            m_mstore32(ref(ancWord) + 4*i, prevIbIndex)
        else:
            fourB = m_getAncestor(hashPrevBlock, i)
            m_mstore32(ref(ancWord) + 4*i, fourB)
        i += 1

    # write the ancestor word to storage
    self.block[blockHash]._ancestor = ancWord


# returns 1 if 'txBlockHash' is in the main chain, ie not a fork
# otherwise returns 0
def inMainChain(txBlockHash):
    txBlockHeight = self.block[txBlockHash]._height

    # By assuming that a block with height 0 does not exist, we can do
    # this optimization and immediate say that txBlockHash is not in the main chain.
    # However, the consequence is that
    # the genesis block must be at height 1 instead of 0 [see setInitialParent()]
    if !txBlockHeight:
        return(0)

    blockHash = self.heaviestBlock

    anc_index = self.numAncestorDepths - 1
    while self.block[blockHash]._height > txBlockHeight:
        while self.block[blockHash]._height - txBlockHeight < self.ancestor_depths[anc_index] && anc_index > 0:
            anc_index -= 1
        blockHash = self.internalBlock[m_getAncestor(blockHash, anc_index)]

    return(blockHash == txBlockHash)


macro m_mstore32($addr, $fourBytes):
    mstore8($addr, byte(31, $fourBytes))
    mstore8($addr + 1, byte(30, $fourBytes))
    mstore8($addr + 2, byte(29, $fourBytes))
    mstore8($addr + 3, byte(28, $fourBytes))


# a block's _ancestor storage slot contains 8 indexes into internalBlock, so
# this macro returns the index that can be used to lookup the desired ancestor
# eg. for combined usage, self.internalBlock[m_getAncestor(someBlock, 2)] will
# return the block hash of someBlock's 3rd ancestor
macro m_getAncestor($blockHash, $anc_index):
    $wordOfAncestorIndexes = self.block[$blockHash]._ancestor
    $startInd = $anc_index * 4
    $b0 = byte($startInd, $wordOfAncestorIndexes)
    $b1 = byte($startInd + 1, $wordOfAncestorIndexes)
    $b2 = byte($startInd + 2, $wordOfAncestorIndexes)
    $b3 = byte($startInd + 3, $wordOfAncestorIndexes)

    $b0 + $b1*256 + $b2*TWOTO16 + $b3*TWOTO24

    # self.block[$blockHash]._ancestor[$anc_index]

macro TWOTO16: 65536
macro TWOTO24: 16777216

# log ancestors
# def logAnc(blockHash):
#     log(11111)
#     log(blockHash)
#     i = 0
#     while i < self.numAncestorDepths:
#         anc = m_getAncestor(blockHash, i)
#         # anc = self.block[blockHash]._ancestor[i]
#         log(anc)
#         i += 1
#     log(22222)
