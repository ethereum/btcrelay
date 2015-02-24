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



###############################################################################
# replace with inset when inset works (eg serpent issue #63)
# inset('btcChain.py')



data numAncestorDepths
self.numAncestorDepths = 9  # if change, look at defn of ancestor_depths and block in btcrelay.py
data ancestor_depths[9]

self.ancestor_depths[0] = 1
self.ancestor_depths[1] = 4
self.ancestor_depths[2] = 16
self.ancestor_depths[3] = 64
self.ancestor_depths[4] = 256
self.ancestor_depths[5] = 1024
self.ancestor_depths[6] = 4096
self.ancestor_depths[7] = 16384
self.ancestor_depths[8] = 65536


# save the ancestors for a block, as well as updating the height
def saveAncestors(blockHash, hashPrevBlock):
    # self.block[blockHash]._prevBlock = hashPrevBlock

    # this is a test; separate genesis function could help later
    # if blockHash == 1:
    #     self.block[blockHash]._height = 1
    # else:
    self.block[blockHash]._height = self.block[hashPrevBlock]._height + 1

    self.block[blockHash]._ancestor[0] = hashPrevBlock
    i = 1
    while i < self.numAncestorDepths:
        depth = self.ancestor_depths[i]

        if self.block[blockHash]._height % depth == 1:
            self.block[blockHash]._ancestor[i] = hashPrevBlock
        else:
            self.block[blockHash]._ancestor[i] = self.block[hashPrevBlock]._ancestor[i]
        i += 1

# in chain:
#     b = head
#     anc_index = ancestor_count - 1
#     while b.number > block.number:
#         while b.number - block.number < ancestor_depths[anc_index] and anc_index > 0:
#             anc_index -= 1
#         b = b.ancestors[anc_index]
#     return b == block


def inMainChain(txBlockHash):
    txBlockHeight = self.block[txBlockHash]._height
    if !txBlockHeight:
        return(0)

    blockHash = self.heaviestBlock

    anc_index = self.numAncestorDepths - 1
    while self.block[blockHash]._height > txBlockHeight:
        while self.block[blockHash]._height - txBlockHeight < self.ancestor_depths[anc_index] && anc_index > 0:
            anc_index -= 1
        blockHash = self.block[blockHash]._ancestor[anc_index]

    return(blockHash == txBlockHash)


def logAnc(blockHash):
    log(11111)
    log(blockHash)
    i = 0
    while i < self.numAncestorDepths:
        anc = self.block[blockHash]._ancestor[i]
        log(anc)
        i += 1
    log(22222)


def logBlockchainHead():
    log(self.heaviestBlock)
    return(self.heaviestBlock)



###############################################################################



# block with the highest score (the end of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore

# note: _ancestor[9]
data block[2^256](_height, _score, _ancestor[9], _blockHeader[])

extern btc_eth: [processTransfer:s:i]


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


def storeBlockHeader(blockHeaderBinary:str):
    # this check can be removed to allow older block headers to be added, but it
    # may provide an attack vector where the contract can be spammed with valid
    # headers that will not be used and simply take up memory storage
    # if hashPrevBlock != self.heaviestBlock:  # special case for genesis prev block of 0 is not needed since self.heaviestBlock is 0 initially
    #     return(0)

    blockHash = self.fastHashBlock(blockHeaderBinary)

    # log(333)
    # log(blockHash)

    bits = getBytesLE(blockHeaderBinary, 4, 72)
    target = targetFromBits(bits)

    difficulty = DIFFICULTY_1 / target # https://en.bitcoin.it/wiki/Difficulty

    # TODO other validation of block?  eg timestamp

    if gt(blockHash, 0) && lt(blockHash, target):  #TODO should sgt and slt be used?

        hashPrevBlock = getBytesLE(blockHeaderBinary, 32, 4)

        self.saveAncestors(blockHash, hashPrevBlock)

        save(self.block[blockHash]._blockHeader[0], blockHeaderBinary, chars=80) # or 160?

        self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty

        if gt(self.block[blockHash]._score, highScore):  #TODO use sgt?
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


macro getPrevBlock($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    getBytesLE($tmpStr, 32, 4)


macro getMerkleRoot($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    getBytesLE($tmpStr, 32, 36)


def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
        return(0)

    merkle = self.computeMerkle(tx, proofLen, hash, path)
    realMerkleRoot = getMerkleRoot(txBlockHash)

    if merkle == realMerkleRoot:
        return(1)
    else:
        return(0)


#TODO txHash can eventually be computed (dbl sha256 then flip32Bytes) when
# txStr becomes txBinary
def relayTx(txStr:str, txHash, proofLen, hash:arr, path:arr, txBlockHash, contract):
    if self.verifyTx(txHash, proofLen, hash, path, txBlockHash) == 1:
        res = contract.processTransfer(txStr)
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

        # blockHash = self.block[blockHash]._prevBlock
        blockHash = getPrevBlock(blockHash)
        i += 1

    return(0)


# little endian get $size bytes from $inStr with $offset
macro getBytesLE($inStr, $size, $offset):
    $endIndex = $offset + $size

    $result = 0
    $exponent = 0
    $j = $offset
    while $j < $endIndex:
        $char = getch($inStr, $j)
        # log($char)
        $result += $char * 256^$exponent
        # log(result)

        $j += 1
        $exponent += 1

    $result


macro concatHash($tx1, $tx2):
    $left = flip32Bytes($tx1)
    $right = flip32Bytes($tx2)

    $hash1 = sha256([$left, $right], chars=64)
    $hash2 = sha256([$hash1], items=1)

    flip32Bytes($hash2)
