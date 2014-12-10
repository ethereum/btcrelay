# Stored variables:
#
# Last known block
# 10: version
# 11: hashPrevBlock
# 12: hashMerkleRoot
# 13: time
# 14: bits
# 15: nonce
# 16: blockHash / lastKnownBlock
# 17: score
#

init:
    self.storage[16] = 0x00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d

code:
    return
