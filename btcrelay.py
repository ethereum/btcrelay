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

data lastKnownBlock
data block[2^256](_height, _blockHeader(_version, _prevBlock, _mrklRoot, _time, _bits, _nonce))


#self.block.blockHeader[]

def shared():
    TWO_POW_24 = 2 ^ 24
    ZEROS = 0x0000000000000000000000000000000000000000000000000000000000000000
    LEFT_HASH = 1
    RIGHT_HASH = 2

def init():
    self.init333k()

def code():
    ret = self.shiftLeft(2,4)
    return(ret)

def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    if hashPrevBlock != self.lastKnownBlock:
        return(0)

    blockHash = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    target = self.targetFromBits(bits)

    # TODO other validation of block?  eg timestamp

    if lt(hash, target):
        self.block[blockHash]._height = self.block[self.lastKnownBlock]._height + 1

        self.block[blockHash]._blockHeader._version = version
        self.block[blockHash]._blockHeader._prevBlock = hashPrevBlock
        self.block[blockHash]._blockHeader._mrklRoot = hashMerkleRoot
        self.block[blockHash]._blockHeader._time = time
        self.block[blockHash]._blockHeader._bits = bits
        self.block[blockHash]._blockHeader._nonce = nonce

        self.lastKnownBlock = blockHash

        return(self.block[blockHash]._height)

    return(0)



def flipBytes(n, numByte):
    mask = 0xff

    result = 0
    i = 0
    while i < numByte:
        b = n & mask
        b = div(b, 2^(i*8))
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
    res = self.testWithin6Confirms()
    return(res)


def isNonceValid(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    target = self.targetFromBits(bits)

    hash = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)

    if lt(hash, target):
        return(1)
    else:
        return(0)


def targetFromBits(bits):
    exp = div(bits, TWO_POW_24)
    mant = bits & 0xffffff
    target = mant * self.shiftLeft(1, (8*(exp - 3)))
    return(target)


def hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    version = self.flipBytes(version, 4)
    hashPrevBlock = self.flipBytes(hashPrevBlock, 32)
    hashMerkleRoot = self.flipBytes(hashMerkleRoot, 32)
    time = self.flipBytes(time, 4)
    bits = self.flipBytes(bits, 4)
    nonce = self.flipBytes(nonce, 4)

    hash = self.__rawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(self.flipBytes(hash, 32))

def __rawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
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


def verifyTx(tx, proofLen, hash:a, path:a, txBlockHash):

    #return(self.block[txBlockHash]._blockHeader._mrklRoot)

    if self.within6Confirms(txBlockHash):
        return(90)

    merkle = self.computeMerkle(tx, proofLen, hash:proofLen, path:proofLen)

    if merkle == self.block[txBlockHash]._blockHeader._mrklRoot:
        return(1)
    else:
        return(0)

# def testVerifyTx():
#     self.testAt6thConfirmVerifyTx()
#     valid = self.testAt7thConfirmVerifyTx()
#     return(valid)
#     return(valid == 1)

def testWithin6Confirms():
    self.init333k()
    b0 = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    b1 = 0x000000000000000010e318d0c61da0b84246481d9cc097fda9327fe90b1538c1 # block #333001
    b2 = 0x000000000000000005895c1348171a774e11ee57374680b54a982e9d9e7309a1
    b3 = 0x00000000000000001348f0e7b14d82d8105992f0968faeb533a03c55c3d72365
    b4 = 0x000000000000000004001d114c6c278eb0ad37a3ce3a111cf534dd358896c5b3
    b5 = 0x000000000000000004860a07b991a6cd7cae1327c36c21903b8bbe8d2c316ac5
    b6 = 0x0000000000000000016f889a84b7a06e2d4d90cec924400cf62a6ca3ae67dd46

    self.lastKnownBlock = b6

    self.block[b6]._blockHeader._prevBlock = b5
    self.block[b5]._blockHeader._prevBlock = b4
    self.block[b4]._blockHeader._prevBlock = b3
    self.block[b3]._blockHeader._prevBlock = b2
    self.block[b2]._blockHeader._prevBlock = b1
    self.block[b1]._blockHeader._prevBlock = b0

    expB6 = self.within6Confirms(b6) == 1
    expB5 = self.within6Confirms(b5) == 1
    expB1 = self.within6Confirms(b1) == 1
    expB0 = self.within6Confirms(b0) == 0

    return(expB6 and expB5 and expB1 and expB0)

# def testAt7thConfirmVerifyTx():
#     self.init333k()
#     b0 = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
#     b1 = 0x000000000000000015873421af098d4d286bf38a1bf1fdac8fda3674fdb8ac04 # block #333001
#     b2 = 0x000000000000000002c29d17ccb9ebc85ee9fd495d19fe9d2ed73f246dd28d99
#     b3 = 0x00000000000000000088be09d237453389d088f5159370ff76be415d53bdd565
#     b4 = 0x00000000000000001567e5b961490f0ecc6449deba7a0f3e0eb7531979892c09
#     b5 = 0x00000000000000001b3b2cbe493085372ad5012e7993d04c455115d65f78e971
#     b6 = 0x00000000000000001567e5b961490f0ecc6449deba7a0f3e0eb7531979892c09
#
#     self.lastKnownBlock = b6
#
#     self.block[b6]._blockHeader._prevBlock = b5
#     self.block[b5]._blockHeader._prevBlock = b4
#     self.block[b4]._blockHeader._prevBlock = b3
#     self.block[b3]._blockHeader._prevBlock = b2
#     self.block[b2]._blockHeader._prevBlock = b1
#     self.block[b1]._blockHeader._prevBlock = b0
#
#     txBlockHash = b0
#     return self.verifyTx(tx, proofLen, hash:a, path:a, txBlockHash)
#
# def testAt6thConfirmVerifyTx():
#     self.init333k()
#     b0 = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
#     b1 = 0x000000000000000015873421af098d4d286bf38a1bf1fdac8fda3674fdb8ac04 # block #333001
#     b2 = 0x000000000000000002c29d17ccb9ebc85ee9fd495d19fe9d2ed73f246dd28d99
#     b3 = 0x00000000000000000088be09d237453389d088f5159370ff76be415d53bdd565
#     b4 = 0x00000000000000001567e5b961490f0ecc6449deba7a0f3e0eb7531979892c09
#     b5 = 0x00000000000000001b3b2cbe493085372ad5012e7993d04c455115d65f78e971
#
#     self.lastKnownBlock = b5
#
#     self.block[b5]._blockHeader._prevBlock = b4
#     self.block[b4]._blockHeader._prevBlock = b3
#     self.block[b3]._blockHeader._prevBlock = b2
#     self.block[b2]._blockHeader._prevBlock = b1
#     self.block[b1]._blockHeader._prevBlock = b0
#
#     txBlockHash = b0
#     return self.verifyTx(tx, proofLen, hash:a, path:a, txBlockHash)


def computeMerkle(tx, proofLen, hash:a, path:a):
    resultHash = tx
    i = 0
    while i < proofLen:
        proofHex = hash[i]
        if path[i] == LEFT_HASH:
            left = proofHex
            right = resultHash
        elif path[i] == RIGHT_HASH:
            left = resultHash
            right = proofHex

        resultHash = self.concatHash(left, right)
        i += 1

    return(resultHash)

def testComputeMerkle():
    # values are from block 100K
    tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    proofLen = 2
    hash = array(proofLen)
    path = array(proofLen)

    hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    path[0] = RIGHT_HASH

    hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
    path[1] = RIGHT_HASH

    r = self.computeMerkle(tx, proofLen, hash:proofLen, path:proofLen)
    expMerkle = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
    return(r == expMerkle)

def within6Confirms(txBlockHash):
    blockHash = self.lastKnownBlock

    i = 0
    while i < 6:
        if txBlockHash == blockHash:
            return(1)

        blockHash = self.block[blockHash]._blockHeader._prevBlock
        i += 1

    return(0)

def concatHash(tx1, tx2):
    left = self.flipBytes(tx1, 32)
    right = self.flipBytes(tx2, 32)

    hash1 = sha256([left, right], chars=64)
    hash2 = sha256([hash1], 1)

    return(self.flipBytes(hash2, 32))

def testConcatHash():
    tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    r = self.concatHash(tx1, tx2)
    return(r == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815)

def testStoreBlockHeader():
    self.init333k()
    version = 2
    hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
    time = 1417792088
    bits = 0x181b7b74
    nonce = 796195988
    blockNumber = 333001

    return(blockNumber == self.storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce))


def testHashHeader():
    version = 2
    hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
    time = 1417792088
    bits = 0x181b7b74
    nonce = 796195988

    expBlockHash = 0x000000000000000010e318d0c61da0b84246481d9cc097fda9327fe90b1538c1
    blockHash = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(blockHash == expBlockHash)


def test__rawHashBlockHeader():
    # https://en.bitcoin.it/wiki/Block_hashing_algorithm
    version = 0x01000000
    hashPrevBlock = 0x81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000
    hashMerkleRoot = 0xe320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b
    time = 0xc7f5d74d
    bits = 0xf2b9441a
    nonce = 0x42a14695

    # these should be the intermediate b1,b2,b3 values inside __rawHashBlockHeader()
    # b1 = 0x0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    # b2 = 0x00000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    # b3 = 0xf1fc122bc7f5d74df2b9441a42a1469500000000000000000000000000000000
    # hash1 = sha256([b1,b2,b3], chars=80)
    # hash2 = sha256([hash1], 1)
    # return(hash2)

    expHash = 0x1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000
    return expHash == self.__rawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)

def init333k():
    self.lastKnownBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    trustedBlock = self.lastKnownBlock
    self.block[trustedBlock]._height = 333000
    self.block[trustedBlock]._blockHeader._version = 2

def testIsNonceValid():
    ver = 2
    prev_block = 0x000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717
    mrkl_root = 0x871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a
    time_ = 0x53058b35 # 2014-02-20 04:57:25
    bits = 0x19015f53
    nonce = 856192328

    res = self.isNonceValid(ver, prev_block, mrkl_root, time_, bits, nonce)
    return(res)
