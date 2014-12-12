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
    ZEROS = 0x0000000000000000000000000000000000000000000000000000000000000000

def init():
    self.storage[16] = 0x00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d

def code():
    ret = self.slt(2,4)
    return(ret)

def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    exp = bits / TWO_POW_24
    mant = bits & 0xffffff
    target = mant * slt(1, (8*(exp - 3)))  # slt ok or need different func?




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

# shift right
def srt(n, x):
    return(div(n, 2^x))

# pad with trailing zeros
#def rpad(val, numZero):


def test():
    # b1 = 0x0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    # b2 = 0x00000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    # b3 = 0xf1fc122bc7f5d74df2b9441a42a1469500000000000000000000000000000000
    # hash1 = sha256([b1,b2,b3], chars=80)
    # hash2 = sha256([hash1], 1)
    # return(hash2)

    version = 0x01000000
    hashPrevBlock = 0x81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000
    hashMerkleRoot = 0xe320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b
    time = 0xc7f5d74d
    bits = 0xf2b9441a
    nonce = 0x42a14695


    verPart = self.slt(version, 28*8)
    hpb28 = self.srt(hashPrevBlock, 4*8)  # 81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    b1 = verPart | hpb28

    hpbLast4 = self.slt(hashPrevBlock, 28*8)  # 000000000
    hm28 = self.srt(hashMerkleRoot, 4*8)  # e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    b2 = hpbLast4 | hm28

    hmLast4 = self.slt(hashMerkleRoot, 28*8)
    timePart = ZEROS | self.slt(time, 24*8)
    bitsPart = ZEROS | self.slt(bits, 20*8)
    noncePart = ZEROS | self.slt(nonce, 16*8)
    b3 = hmLast4 | timePart | bitsPart | noncePart

    hash1 = sha256([b1,b2,b3], chars=80)
    hash2 = sha256([hash1], 1)
    return(hash2)
