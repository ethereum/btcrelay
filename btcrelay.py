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

shared:
    TWO_POW_24 = 2 ^ 24

init:
    self.storage[16] = 0x00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d

code:
    def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
        exp = bits / TWO_POW_24
        mant = bits & 0xffffff
        target = mant * slt(1, (8*(exp - 3)))

    # shift left
    def slt(n, x):
        return(n * 2^x)
