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

def shared():
    TWO_POW_24 = 2 ^ 24

def init():
    self.storage[16] = 0x00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d

def code():
    ret = self.slt(2,4)
    return(ret)

def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    exp = bits / TWO_POW_24
    mant = bits & 0xffffff
    target = mant * slt(1, (8*(exp - 3)))


def flipBytes(n):
    numByte = 32
    mask = 0xff

    result = 0
    i = 0
    while i < numByte:
        b = n & mask
        b /= 2^(i*8)
        b *= 2^((numByte-i-1)*8)
        mask *= 256
        result = result | b
        i += 1

    return(result)

# shift left
def slt(n, x):
    return(n * 2^x)


def test():
    b1 = 0x0100000081cd02ab7e569e8bcd9317e2
    b2 = 0xfe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b
    b3 = 0x1eb942ae710e951ed797f7affc8892b0f1fc122bc7f5d74df2b9441a42a14695
    hash1 = sha256([b1,b2,b3], 3)
    hash2 = sha256([hash1], 1)
    return(hash2)
