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

inset('btcChain.py')

# block with the highest score (the end of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore

# note: _ancestor[9]
#TODO _prevBlock is redundant but may save on gas instead of repeated lookups for it inside of _blockHeader
data block[2^256](_height, _score, _ancestor[9], _blockHeader[], _prevBlock)

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

        # hashPrevBlock = stringReadUnsignedBitsLE(rawBlockHeader, 256, 4)

        self.saveAncestors(blockHash, hashPrevBlock)

        log(datastr=blockHeaderBinary)
        save(self.block[blockHash]._blockHeader[0], blockHeaderBinary, chars=80) # or 160?

        tmpStr = load(self.block[blockHash]._blockHeader[0], chars=80)
        log(datastr=tmpStr)
        realMerkleRoot = jjj(tmpStr, 32, 36)
        log(44444)
        log(realMerkleRoot)

        self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty

        if gt(self.block[blockHash]._score, highScore):
            self.heaviestBlock = blockHash
            highScore = self.block[blockHash]._score

        return(self.block[blockHash]._height)

    return(0)

def fastHashBlock(blockHeaderBinary:str):
    hash1 = sha256(blockHeaderBinary:str)
    hash2 = sha256(hash1)
    res = flip32Bytes(hash2)
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

macro flip32Bytes($a):
    $o = 0
    with $i = 0:
        while $i < 32:
            mstore8(ref($o) + $i, byte(31 - $i, $a))
            $i += 1
    $o

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


# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
macro targetFromBits($bits):
    $exp = div($bits, TWO_POW_24)
    $mant = $bits & 0xffffff
    $target = $mant * shiftLeftBytes(1, ($exp - 3))
    $target



def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
        return(0)

    merkle = self.computeMerkle(tx, proofLen, hash, path)

    tmpStr = load(self.block[txBlockHash]._blockHeader[0], chars=160)
    realMerkleRoot = jjj(tmpStr, 32, 36)

    log(999)
    log(merkle)
    log(realMerkleRoot)

    if merkle == realMarkleRoot:
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

        blockHash = self.block[blockHash]._prevBlock
        i += 1

    return(0)


macro jjj($inStr, $bytes, $pos):
    $size = $bytes
    $offset = $pos
    $endIndex = $offset + $size

    $result = 0
    $exponent = 0
    $j = $offset
    while $j < $endIndex:
        # "01 23 45" want it to read "10 32 54"
        # if $j % 2 == 0:
        #     $i = $j + 1
        # else:
        #     $i = $j - 1

        $i = $j

        $char = getch($inStr, $i)
        # log($char)

        # if ($char >= 97 && $char <= 102):  # only handles lowercase a-f
        #     $numeric = $char - 87
        # else:
        #     $numeric = $char - 48

        # log(numeric)

        $result += $char * 256^$exponent
        # log(result)

        $j += 1
        $exponent += 1

    # return(result)

    $result


# only handles lowercase a-f
# tested via hashBlock()
macro stringReadUnsignedBitsLE($inStr, $bits, $pos):
    $size = $bits / 4
    $offset = $pos * 2  #TODO remove the *2?
    $endIndex = $offset + $size

    $result = 0
    $exponent = 0
    $j = $offset
    while $j < $endIndex:
        # "01 23 45" want it to read "10 32 54"
        if $j % 2 == 0:
            $i = $j + 1
        else:
            $i = $j - 1

        $char = getch($inStr, $i)
        log($char)
        if ($char >= 97 && $char <= 102):  # only handles lowercase a-f
            $numeric = $char - 87
        else:
            $numeric = $char - 48

        # log(numeric)

        $result += $numeric * 16^$exponent
        # log(result)

        $j += 1
        $exponent += 1

    # return(result)

    $result


macro concatHash($tx1, $tx2):
    $left = flip32Bytes($tx1)
    $right = flip32Bytes($tx2)

    $hash1 = sha256([$left, $right], chars=64)
    $hash2 = sha256([$hash1], items=1)

    flip32Bytes($hash2)
