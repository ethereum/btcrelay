# this is disabled because inset() doesn't work per Serpent issue #63
#
# data numAncestorDepths
# self.numAncestorDepths = 9  # if change, look at defn of ancestor_depths and block in btcrelay.py
# data ancestor_depths[9]
#
# self.ancestor_depths[0] = 1
# self.ancestor_depths[1] = 4
# self.ancestor_depths[2] = 16
# self.ancestor_depths[3] = 64
# self.ancestor_depths[4] = 256
# self.ancestor_depths[5] = 1024
# self.ancestor_depths[6] = 4096
# self.ancestor_depths[7] = 16384
# self.ancestor_depths[8] = 65536
#
#
# # save the ancestors for a block, as well as updating the height
# def saveAncestors(blockHash, hashPrevBlock):
#     # self.block[blockHash]._prevBlock = hashPrevBlock
#
#     # this is a test; separate genesis function could help later
#     # if blockHash == 1:
#     #     self.block[blockHash]._height = 1
#     # else:
#     self.block[blockHash]._height = self.block[hashPrevBlock]._height + 1
#
#     self.block[blockHash]._ancestor[0] = hashPrevBlock
#     i = 1
#     while i < self.numAncestorDepths:
#         depth = self.ancestor_depths[i]
#
#         if self.block[blockHash]._height % depth == 1:
#             self.block[blockHash]._ancestor[i] = hashPrevBlock
#         else:
#             self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i]
#         i += 1
#
# # in chain:
# #     b = head
# #     anc_index = ancestor_count - 1
# #     while b.number > block.number:
# #         while b.number - block.number < ancestor_depths[anc_index] and anc_index > 0:
# #             anc_index -= 1
# #         b = b.ancestors[anc_index]
# #     return b == block
#
#
# def inMainChain(txBlockHash):
#     txBlockHeight = self.block[txBlockHash]._height
#     if !txBlockHeight:
#         return(0)
#
#     blockHash = self.heaviestBlock
#
#     anc_index = self.numAncestorDepths - 1
#     while self.block[blockHash]._height > txBlockHeight:
#         while self.block[blockHash]._height - txBlockHeight < self.ancestor_depths[anc_index] && anc_index > 0:
#             anc_index -= 1
#         blockHash = self.block[blockHash]._ancestor[anc_index]
#
#     return(blockHash == txBlockHash)
#
#
# def logAnc(blockHash):
#     log(11111)
#     log(blockHash)
#     i = 0
#     while i < self.numAncestorDepths:
#         anc = self.block[blockHash]._ancestor[i]
#         log(anc)
#         i += 1
#     log(22222)
#
#
# def logBlockchainHead():
#     log(self.heaviestBlock)
#     return(self.heaviestBlock)
