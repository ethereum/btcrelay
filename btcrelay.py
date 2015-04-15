
inset('btcChain.py')


# btcrelay can relay a transaction to any contract that has a function
# name 'processTransaction' with signature si:i
extern relayDestination: [processTransaction:si:i]


# note: _ancestor[9]
#
# a Bitcoin block (header) is stored as:
# - _blockHeader 80 bytes
# - _height is 1 more than the typical Bitcoin term height/blocknumber [see setPreGensesis()]
# - _score is 1 more than the cumulative difficulty [see setPreGenesis()]
# - _ancestor list for more efficient backtracking (see btcChain)
data block[2^256](_height, _score, _ancestor[9], _blockHeader[])


# block with the highest score (aka the Head of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore


# def init():
    # TODO anything else to init ?


#TODO for testing only; should be omitted for production
def testingonlySetHeaviest(blockHash):
    self.heaviestBlock = blockHash


# this has 2 purposes:
# 1) this can only be called once and is to "store" the block
# with hash zeroes, so that storing the real genesis
# block can be done using storeBlockHeader() instead of a special case
#
# 2) allows testing of storing arbitrary headers and verifying/relaying
# transactions, say from block 300K, instead
# of Satoshi's genesis block which have 0 transactions until much later on
#
# Since zero is the value that indicates non-existence, block _height
# and _score have to be set carefully and they have these consequences:
#
# - _height is 1 more than the typical Bitcoin
# term height/blocknumber. ie genesis has height 1 instead of 0
#
# - _score is 1 more than the cumulative "Bitcoin standard
# difficulty". eg the cumulative difficulty at the block after genesis
# is 2 (it and genesis have difficulty of 1), but this contract assigns
# a score of 3 for the block after genesis [see testStoringHeaders()]
def setPreGenesis(blockHash):
    # reuse highScore as the flag for whether setPreGenesis() has already been called
    if self.highScore != 0:
        return(0)
    else:
        self.highScore = 1  # matches the score that is set below in this function

    self.heaviestBlock = blockHash

    # _height cannot be set to -1 because inMainChain() assumes that
    # a block with height0 does NOT exist, thus we cannot allow the
    # real genesis block to be at height0
    self.block[blockHash]._height = 0

    # set score to 1, since score0 means block does NOT exist. see check in storeBlockHeader()
    # this means that the score of a block is 1 more than the
    # cumulative difficulty to that block
    self.block[blockHash]._score = 1

    ancLen = self.numAncestorDepths
    i = 0
    while i < ancLen:
        self.block[blockHash]._ancestor[i] = blockHash
        i += 1

    return(1)


# store a Bitcoin block header that must be provided in
# binary format 'blockHeaderBinary'
def storeBlockHeader(blockHeaderBinary:str):
    hashPrevBlock = flip32Bytes(~calldataload(40))  # 36 (header start) + 4 (offset for hashPrevBlock)

    assert self.block[hashPrevBlock]._score  # score0 means block does NOT exist; genesis has score of 1

    blockHash = self.fastHashBlock(blockHeaderBinary)

    if self.block[blockHash]._score != 0:  # block already exists
        return(0)

    bits = getBytesLE(blockHeaderBinary, 4, 72)
    target = targetFromBits(bits)

    # we only check the target and do not do other validation (eg timestamp)
    # to save gas
    if gt(blockHash, 0) && lt(blockHash, target):
        self.saveAncestors(blockHash, hashPrevBlock)

        save(self.block[blockHash]._blockHeader[0], blockHeaderBinary, chars=80) # or 160?

        difficulty = 0x00000000FFFF0000000000000000000000000000000000000000000000000000 / target # https://en.bitcoin.it/wiki/Difficulty
        self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty

        if gt(self.block[blockHash]._score, self.highScore):
            self.heaviestBlock = blockHash
            self.highScore = self.block[blockHash]._score

        return(self.block[blockHash]._height)

    return(0)


# returns 1 if tx is in the block given by 'txBlockHash' and the block is
# in Bitcoin's main chain (ie not a fork)
#
# the merkle proof is represented by 'proofLen', 'hash', 'path', where:
# - 'hash' are the merkle siblings of tx
# - 'path' corresponds to whether the sibling is to the LEFT (1) or RIGHT (2)
# - 'proofLen' is the number of merkle siblings
def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
        return(0)

    merkle = self.computeMerkle(tx, proofLen, hash, path)
    realMerkleRoot = getMerkleRoot(txBlockHash)

    if merkle == realMerkleRoot:
        return(1)
    else:
        return(0)


# returns the value of processTransaction().  callers should explicitly
# check for a value of 1, since other non-zero values could be error codes
#
# TODO txHash can eventually be computed (dbl sha256 then flip32Bytes) when
# txStr becomes txBinary
def relayTx(txStr:str, txHash, proofLen, hash:arr, path:arr, txBlockHash, contract):
    if self.verifyTx(txHash, proofLen, hash, path, txBlockHash) == 1:
        res = contract.processTransaction(txStr, txHash)
        return(res)
    return(0)


# return the difference between the cumulative difficulty at
# the blockchain Head and its 10th ancestor
def getAverageBlockDifficulty():
    blockHash = self.heaviestBlock

    cumulDifficultyHead = self.block[blockHash]._score - 1

    i = 0
    while i < 10:
        blockHash = getPrevBlock(blockHash)
        i += 1

    cumulDifficulty10Ancestors = self.block[blockHash]._score - 1

    return(cumulDifficultyHead - cumulDifficulty10Ancestors)


# return the hash of the heaviest block aka the Head
def getBlockchainHead():
    # log(self.heaviestBlock)
    return(self.heaviestBlock)


# return the (total) cumulative difficulty of the Head
def getCumulativeDifficulty():
    # Because of setPreGenesis(), the score is 1 more than than the
    # cumulative difficulty
    cumulDifficulty = self.block[self.heaviestBlock]._score - 1
    return(cumulDifficulty)


# return -1 if there's an error (eg called with incorrect params)
# [see documentation for verifyTx() for the merkle proof
# format of 'proofLen', 'hash', 'path' ]
def computeMerkle(tx, proofLen, hash:arr, path:arr):
    LEFT_HASH = 1
    RIGHT_HASH = 2

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


# returns 1 if the 'txBlockHash' is within 6 blocks of self.heaviestBlock
# otherwise returns 0.
# note: return value of 0 does not mean 'txBlockHash' has more than 6
# confirmations; a non-existent 'txBlockHash' will lead to a return value of 0
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


# Bitcoin-way of hashing a block header
def fastHashBlock(blockHeaderBinary:str):
    return(flip32Bytes(sha256(sha256(blockHeaderBinary:str))))



#
# macros
#

# get the parent of '$blockHash'
macro getPrevBlock($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=36)  # don't need all 80bytes
    getBytesLE($tmpStr, 32, 4)


# get the merkle root of '$blockHash'
macro getMerkleRoot($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=68)  # don't need all 80bytes
    getBytesLE($tmpStr, 32, 36)


# get $size bytes from $inStr with $offset and return in little endian
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


# Bitcoin-way of computing the target from the 'bits' field of a blockheader
# based on http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
macro targetFromBits($bits):
    $exp = div($bits, 0x1000000)  # 2^24
    $mant = $bits & 0xffffff
    $mant * 256^($exp - 3)


# Bitcoin-way merkle parent of transaction hashes $tx1 and $tx2
macro concatHash($tx1, $tx2):
    with $x = ~alloc(64):
        ~mstore($x, flip32Bytes($tx1))
        ~mstore($x + 32, flip32Bytes($tx2))
        flip32Bytes(sha256(sha256($x, chars=64)))


# reverse 32 bytes given by '$b32'
macro flip32Bytes($b32):
    with $a = $b32:  # important to force $a to only be examined once below
        $o = 0
        mstore8(ref($o), byte(31, $a))
        mstore8(ref($o) + 1,  byte(30, $a))
        mstore8(ref($o) + 2,  byte(29, $a))
        mstore8(ref($o) + 3,  byte(28, $a))
        mstore8(ref($o) + 4,  byte(27, $a))
        mstore8(ref($o) + 5,  byte(26, $a))
        mstore8(ref($o) + 6,  byte(25, $a))
        mstore8(ref($o) + 7,  byte(24, $a))
        mstore8(ref($o) + 8,  byte(23, $a))
        mstore8(ref($o) + 9,  byte(22, $a))
        mstore8(ref($o) + 10, byte(21, $a))
        mstore8(ref($o) + 11, byte(20, $a))
        mstore8(ref($o) + 12, byte(19, $a))
        mstore8(ref($o) + 13, byte(18, $a))
        mstore8(ref($o) + 14, byte(17, $a))
        mstore8(ref($o) + 15, byte(16, $a))
        mstore8(ref($o) + 16, byte(15, $a))
        mstore8(ref($o) + 17, byte(14, $a))
        mstore8(ref($o) + 18, byte(13, $a))
        mstore8(ref($o) + 19, byte(12, $a))
        mstore8(ref($o) + 20, byte(11, $a))
        mstore8(ref($o) + 21, byte(10, $a))
        mstore8(ref($o) + 22, byte(9, $a))
        mstore8(ref($o) + 23, byte(8, $a))
        mstore8(ref($o) + 24, byte(7, $a))
        mstore8(ref($o) + 25, byte(6, $a))
        mstore8(ref($o) + 26, byte(5, $a))
        mstore8(ref($o) + 27, byte(4, $a))
        mstore8(ref($o) + 28, byte(3, $a))
        mstore8(ref($o) + 29, byte(2, $a))
        mstore8(ref($o) + 30, byte(1, $a))
        mstore8(ref($o) + 31, byte(0, $a))
        $o
