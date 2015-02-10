# Stored variables:
#
# Last known block
# 10: version
# 11: hashPrevBlock
# 12: hashMerkleRoot
# 13: time
# 14: bits
# 15: nonce
# 16: blockHash / heaviestBlock
# 17: score
#

inset('tryStoreHeaders.py')

# block with the highest score (the end of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore

# note: _ancestor[9]
data block[2^256](_height, _score, _ancestor[9], _blockHeader(_version, _prevBlock, _mrklRoot, _time, _bits, _nonce))

extern btc_eth: [processTransfer:i:i]


#self.block.blockHeader[]

def shared():
    DIFFICULTY_1 = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
    TWO_POW_24 = 2 ^ 24
    ZEROS = 0x0000000000000000000000000000000000000000000000000000000000000000
    LEFT_HASH = 1
    RIGHT_HASH = 2

def init():
    # TODO what to init
    self.init333k()


#TODO for testing only
def init333k():
    self.heaviestBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    trustedBlock = self.heaviestBlock
    self.block[trustedBlock]._height = 333000
    self.block[trustedBlock]._blockHeader._version = 2


#TODO for testing only
def testingonlySetHeaviest(blockHash):
    self.heaviestBlock = blockHash



def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    # this check can be removed to allow older block headers to be added, but it
    # may provide an attack vector where the contract can be spammed with valid
    # headers that will not be used and simply take up memory storage
    if hashPrevBlock != self.heaviestBlock:  # special case for genesis prev block of 0 is not needed since self.heaviestBlock is 0 initially
        return(0)

    blockHash = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    target = self.targetFromBits(bits)

    log(target)

    difficulty = DIFFICULTY_1 / target # https://en.bitcoin.it/wiki/Difficulty

    # TODO other validation of block?  eg timestamp

    if gt(blockHash, 0) && lt(blockHash, target):
        self.saveAncestors(blockHash, hashPrevBlock)

        self.block[blockHash]._blockHeader._version = version
        self.block[blockHash]._blockHeader._mrklRoot = hashMerkleRoot
        self.block[blockHash]._blockHeader._time = time
        self.block[blockHash]._blockHeader._bits = bits
        self.block[blockHash]._blockHeader._nonce = nonce

        self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty

        if gt(self.block[blockHash]._score, highScore):
            self.heaviestBlock = blockHash
            highScore = self.block[blockHash]._score

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

    hash = self.doRawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(self.flipBytes(hash, 32))

def doRawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
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
    hash2 = sha256([hash1], items=1)
    return(hash2)


def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if self.within6Confirms(txBlockHash):
        return(0)

    merkle = self.computeMerkle(tx, proofLen, hash, path)

    if merkle == self.block[txBlockHash]._blockHeader._mrklRoot:
        return(1)
    else:
        return(0)

def relayTx(tx, proofLen, hash:arr, path:arr, txBlockHash, contract):
    if self.verifyTx(tx, proofLen, hash, path, txBlockHash) == 1:
        res = contract.processTransfer(13)
        return(res)
        # return(call(contract, tx))
    return(0)


# return -1 if there's an error (eg called with incorrect params)
def computeMerkle(tx, proofLen, hash:arr, path:arr):
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

    if !resultHash:
        return(-1)

    return(resultHash)


def within6Confirms(txBlockHash):
    blockHash = self.heaviestBlock

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
    hash2 = sha256([hash1], items=1)

    return(self.flipBytes(hash2, 32))
