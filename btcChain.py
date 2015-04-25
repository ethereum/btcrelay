# btcChain is required by btcrelay and is a separate file to improve
# clarity: it has ancestor management and its
# main method is inMainChain() which is tested by test_btcChain

data numAncestorDepths
self.numAncestorDepths = 9  # if changing this, need to do so carefully eg look at defn of ancestor_depths and block in btcrelay
data ancestor_depths[9]

self.ancestor_depths[0] = 1
self.ancestor_depths[1] = 4
self.ancestor_depths[2] = 16
self.ancestor_depths[3] = 64
self.ancestor_depths[4] = 256
self.ancestor_depths[5] = 1024
self.ancestor_depths[6] = 4096
self.ancestor_depths[7] = 16384
self.ancestor_depths[8] = 65536


# save the ancestors for a block, as well as updating the height
def saveAncestors(blockHash, hashPrevBlock):
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
        blockHash = self.block[blockHash]._ancestor[anc_index]

    return(blockHash == txBlockHash)


# log ancestors
# def logAnc(blockHash):
#     log(11111)
#     log(blockHash)
#     i = 0
#     while i < self.numAncestorDepths:
#         anc = self.block[blockHash]._ancestor[i]
#         log(anc)
#         i += 1
#     log(22222)
