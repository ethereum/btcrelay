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
    ret = self.shiftLeft(2,4)
    return(ret)

def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    exp = bits / TWO_POW_24
    mant = bits & 0xffffff
    target = mant * shiftLeft(1, (8*(exp - 3)))



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
def shiftLeft(n, x):
    return(n * 2^x)

# shift right
def shiftRight(n, x):
    return(div(n, 2^x))

# pad with trailing zeros
#def rpad(val, numZero):


def test():
    ver = 2
    prev_block = 0x000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717
    mrkl_root = 0x871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a
    time_ = 0x53058b35 # 2014-02-20 04:57:25
    bits = 0x19015f53

    return(self.targetFromBits(bits))

    # res = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    # return(res)


def targetFromBits(bits):
    exp = div(bits, TWO_POW_24)
    mant = bits & 0xffffff
    target = mant * self.shiftLeft(1, (8*(exp - 3)))
    return(target)

def hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    # https://en.bitcoin.it/wiki/Block_hashing_algorithm
    # version = 0x01000000
    # hashPrevBlock = 0x81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000
    # hashMerkleRoot = 0xe320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b
    # time = 0xc7f5d74d
    # bits = 0xf2b9441a
    # nonce = 0x42a14695
    # b1 = 0x0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    # b2 = 0x00000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    # b3 = 0xf1fc122bc7f5d74df2b9441a42a1469500000000000000000000000000000000
    # hash1 = sha256([b1,b2,b3], chars=80)
    # hash2 = sha256([hash1], 1)
    # return(hash2)

    verPart = self.shiftLeft(version, 28*8)
    hpb28 = self.shiftRight(hashPrevBlock, 4*8)  # 81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    b1 = verPart | hpb28

    hpbLast4 = self.shiftLeft(hashPrevBlock, 28*8)  # 000000000
    hm28 = self.shiftRight(hashMerkleRoot, 4*8)  # e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    b2 = hpbLast4 | hm28

    hmLast4 = self.shiftLeft(hashMerkleRoot, 28*8)
    timePart = ZEROS | self.shiftLeft(time, 24*8)
    bitsPart = ZEROS | self.shiftLeft(bits, 20*8)
    noncePart = ZEROS | self.shiftLeft(nonce, 16*8)
    b3 = hmLast4 | timePart | bitsPart | noncePart

    hash1 = sha256([b1,b2,b3], chars=80)
    hash2 = sha256([hash1], 1)
    return(hash2)
