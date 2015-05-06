inset('constants.se')

# btcChain is required by btcrelay and is a separate file to improve
# clarity: it has ancestor management and its
# main method is inMainChain() which is tested by test_btcChain

macro NUM_ANCESTOR_DEPTHS: 8

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
    m_setIbIndex(blockHash, self.ibIndex)
    self.ibIndex += 1

    m_setHeight(blockHash, m_getHeight(hashPrevBlock) + 1)

    # 8 indexes into internalBlock can be stored inside one ancestor (32 byte) word
    ancWord = 0

    # the first ancestor is the index to hashPrevBlock, and write it to ancWord
    prevIbIndex = m_getIbIndex(hashPrevBlock)
    m_mwrite32(ref(ancWord), prevIbIndex)

    # update ancWord with the remaining indexes
    i = 1
    while i < NUM_ANCESTOR_DEPTHS:
        depth = m_getAncDepth(i)

        if m_getHeight(blockHash) % depth == 1:
            m_mwrite32(ref(ancWord) + 4*i, prevIbIndex)
        else:
            m_mwrite32(ref(ancWord) + 4*i, m_getAncestor(hashPrevBlock, i))
        i += 1

    # write the ancestor word to storage
    self.block[blockHash]._ancestor = ancWord


# returns 1 if 'txBlockHash' is in the main chain, ie not a fork
# otherwise returns 0
def inMainChain(txBlockHash):
    txBlockHeight = m_getHeight(txBlockHash)

    # By assuming that a block with height 0 does not exist, we can do
    # this optimization and immediate say that txBlockHash is not in the main chain.
    # However, the consequence is that
    # the genesis block must be at height 1 instead of 0 [see setInitialParent()]
    if !txBlockHeight:
        return(0)

    blockHash = self.heaviestBlock

    anc_index = NUM_ANCESTOR_DEPTHS - 1
    while m_getHeight(blockHash) > txBlockHeight:
        while m_getHeight(blockHash) - txBlockHeight < m_getAncDepth(anc_index) && anc_index > 0:
            anc_index -= 1
        blockHash = self.internalBlock[m_getAncestor(blockHash, anc_index)]

    return(blockHash == txBlockHash)


#
# macros
#

# a block's _ancestor storage slot contains 8 indexes into internalBlock, so
# this macro returns the index that can be used to lookup the desired ancestor
# eg. for combined usage, self.internalBlock[m_getAncestor(someBlock, 2)] will
# return the block hash of someBlock's 3rd ancestor
macro m_getAncestor($blockHash, $whichAncestor):
    div(sload(ref(self.block[$blockHash]._ancestor)) * 2**(32*$whichAncestor), BYTES_28)


# index should be 0 to 7, so this returns 1, 5, 25 ... 78125
macro m_getAncDepth($index):
    5**$index


# write $int32 to memory at $addrLoc
# This is useful for writing 32bit ints inside one 32 byte word
macro m_mwrite32($addrLoc, $int32):
    with $addr = $addrLoc:
        with $fourBytes = $int32:
            mstore8($addr, byte(28, $fourBytes))
            mstore8($addr + 1, byte(29, $fourBytes))
            mstore8($addr + 2, byte(30, $fourBytes))
            mstore8($addr + 3, byte(31, $fourBytes))


# write $int24 to memory at $addrLoc
# This is useful for writing 24bit ints inside one 32 byte word
macro m_mwrite24($addrLoc, $int24):
    with $addr = $addrLoc:
        with $threeBytes = $int24:
            mstore8($addr, byte(29, $threeBytes))
            mstore8($addr + 1, byte(30, $threeBytes))
            mstore8($addr + 2, byte(31, $threeBytes))


# write $int16 to memory at $addrLoc
# This is useful for writing 16bit ints inside one 32 byte word
macro m_mwrite16($addrLoc, $int16):
    with $addr = $addrLoc:
        with $twoBytes = $int16:
            mstore8($addr, byte(30, $twoBytes))
            mstore8($addr + 1, byte(31, $twoBytes))


# log ancestors
# def logAnc(blockHash):
#     log(11111)
#     log(blockHash)
#     i = 0
#     while i < NUM_ANCESTOR_DEPTHS:
#         anc = m_getAncestor(blockHash, i)
#         # anc = self.block[blockHash]._ancestor[i]
#         log(anc)
#         i += 1
#     log(22222)
