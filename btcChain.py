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


# save the ancestors for a block, as well as updating the height
def saveAncestors(blockHash, hashPrevBlock):
    self.block[blockHash]._height = self.block[hashPrevBlock]._height + 1

    ancWord = 0
    m_mstore32(ref(ancWord), hashPrevBlock)
    # mstore8(ref(ancWord), hashPrevBlock)

    # self.block[blockHash]._ancestor[0] = hashPrevBlock
    i = 1
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]

        if self.block[blockHash]._height % depth == 1:
            m_mstore32(ref(ancWord) + 4*i, hashPrevBlock)
            # self.block[blockHash]._ancestor[i] = hashPrevBlock
        else:
            fourB = m_getAncestor(hashPrevBlock, i)
            m_mstore32(ref(ancWord) + 4*i, fourB)
            # self.block[blockHash]._ancestor[i] = m_getAncestor(hashPrevBlock, i)
        i += 1

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
        blockHash = m_getAncestor(blockHash, anc_index)

    return(blockHash == txBlockHash)


macro m_mstore32($addr, $fourBytes):
    mstore8($addr, byte(31, $fourBytes))
    mstore8($addr + 1, byte(30, $fourBytes))
    mstore8($addr + 2, byte(29, $fourBytes))
    mstore8($addr + 3, byte(28, $fourBytes))


macro m_getAncestor($blockHash, $anc_index):
    $startInd = $anc_index*4
    $b0 = byte($startInd, self.block[$blockHash]._ancestor)
    $b1 = byte($startInd + 1, self.block[$blockHash]._ancestor)
    $b2 = byte($startInd + 2, self.block[$blockHash]._ancestor)
    $b3 = byte($startInd + 3, self.block[$blockHash]._ancestor)

    $b0 + $b1*256 + $b2*256^2 + $b3*256^3

    # self.block[$blockHash]._ancestor[$anc_index]


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
