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

#TODO for testing only
def testingonlySetGenesis(blockHash):
    self.heaviestBlock = blockHash
    self.block[blockHash]._height = 1
    ancLen = self.numAncestorDepths
    i = 0
    while i < ancLen:
        self.block[blockHash]._ancestor[i] = blockHash
        i += 1


def storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce, blockHeaderBinary:str):
    # this check can be removed to allow older block headers to be added, but it
    # may provide an attack vector where the contract can be spammed with valid
    # headers that will not be used and simply take up memory storage
    # if hashPrevBlock != self.heaviestBlock:  # special case for genesis prev block of 0 is not needed since self.heaviestBlock is 0 initially
    #     return(0)

    blockHash = self.fastHashBlock(blockHeaderBinary)

    # log(333)
    # log(blockHash)
    
    target = targetFromBits(bits)

    difficulty = DIFFICULTY_1 / target # https://en.bitcoin.it/wiki/Difficulty

    # TODO other validation of block?  eg timestamp

    if gt(blockHash, 0) && lt(blockHash, target):  #TODO should sgt and slt be used?
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

def fastHashBlock(blockHeaderBinary:str):
    hash1 = sha256(blockHeaderBinary:str)
    hash2 = sha256(hash1)
    res = flipBytes(hash2, 32)
    return(res)

# eg 0x6162 will be 0x6261
macro flipBytes($n, $numByte):
    $b = byte(31, $n)

    $i = 30
    $j = 1
    while $j < $numByte:
        $b = ($b * 256) | byte($i, $n)
        $i -= 1
        $j += 1

    $b

# macro optFlip($a):
#     $o = 0
#     with $i = 0:
#         while $i < 32:
#             mstore8(ref($o) + $i, byte(31 - $i, $a))
#             $i += 1
#     $o

# fast string flip bytes
# macro vflip($x, $L):
#     with $o = alloc($L + 32):
#         with $lim = $o + 2:
#             $o += $L
#             with $y = $x - 31:
#                 while $o > $lim:
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                 if $o > $lim - 2:
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                 if $o > $lim - 2:
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#         mstore($o, $L)
#         $o + 32



# shift left bytes
macro shiftLeftBytes($n, $x):
    $n * 256^$x  # set the base to 2 (instead of 256) if we want a macro to shift only bits

# shift right
macro shiftRightBytes($n, $x):
    div($n, 256^$x)


def isNonceValid(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    target = targetFromBits(bits)

    hash = hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)

    if lt(hash, target):
        return(1)
    else:
        return(0)


# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
macro targetFromBits($bits):
    $exp = div($bits, TWO_POW_24)
    $mant = $bits & 0xffffff
    $target = $mant * shiftLeftBytes(1, ($exp - 3))
    $target


macro hashHeader($version, $hashPrevBlock, $hashMerkleRoot, $time, $bits, $nonce):
    $_version = flipBytes($version, 4)
    $_hashPrevBlock = flipBytes($hashPrevBlock, 32)
    $_hashMerkleRoot = flipBytes($hashMerkleRoot, 32)
    $_time = flipBytes($time, 4)
    $_bits = flipBytes($bits, 4)
    $_nonce = flipBytes($nonce, 4)

    $hash = doRawHashBlockHeader($_version, $_hashPrevBlock, $_hashMerkleRoot, $_time, $_bits, $_nonce)
    $retHash = flipBytes($hash, 32)
    $retHash


macro doRawHashBlockHeader($version, $hashPrevBlock, $hashMerkleRoot, $time, $bits, $nonce):
    verPart = shiftLeftBytes($version, 28)
    hpb28 = shiftRightBytes($hashPrevBlock, 4)  # 81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    b1 = verPart | hpb28

    hpbLast4 = shiftLeftBytes($hashPrevBlock, 28)  # 000000000
    hm28 = shiftRightBytes($hashMerkleRoot, 4)  # e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    b2 = hpbLast4 | hm28

    hmLast4 = shiftLeftBytes($hashMerkleRoot, 28)
    timePart = ZEROS | shiftLeftBytes($time, 24)
    bitsPart = ZEROS | shiftLeftBytes($bits, 20)
    noncePart = ZEROS | shiftLeftBytes($nonce, 16)
    b3 = hmLast4 | timePart | bitsPart | noncePart

    hash1 = sha256([b1,b2,b3], chars=80)
    hash2 = sha256([hash1], items=1)
    hash2


def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
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

        resultHash = concatHash(left, right)

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

macro concatHash($tx1, $tx2):
    $left = flipBytes($tx1, 32)
    $right = flipBytes($tx2, 32)

    $hash1 = sha256([$left, $right], chars=64)
    $hash2 = sha256([$hash1], items=1)

    flipBytes($hash2, 32)
