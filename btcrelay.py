
inset('btcChain.py')


# btcrelay can relay a transaction to any contract that has a function
# name 'processTransaction' with signature si:i
extern relayDestination: [processTransaction:si:i]


# note: _ancestor[9]
#
# a Bitcoin block (header) is stored as:
# - _blockHeader 80 bytes
# - _height
# - _score
# - _ancestor list for more efficient backtracking (see btcChain.py)
data block[2^256](_height, _score, _ancestor[9], _blockHeader[])


# block with the highest score (aka the Head of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore

# owner/adminstrator of this contract
data owner


def init():
    self.owner = msg.sender
    # TODO anything else to init ?


#TODO for testing only; should be omitted for production
def testingonlySetHeaviest(blockHash):
    if tx.origin == self.owner:
        self.heaviestBlock = blockHash


# this has 2 purposes:
# 1) this should only be called once and is to "store" the block
# with hash zeroes, so that storing the real genesis
# block can be done using storeBlockHeader() instead of a special case
#
# 2) allows testing of storing arbitrary headers and verifying/relaying
# transactions, say from block 300K, instead
# of Satoshi's genesis block which have 0 transactions until much later on
#
# a consequence of this function is that the score of blocks is
# 1 more than its calculated difficulty
def setPreGenesis(blockHash):
    if tx.origin == self.owner:
        self.heaviestBlock = blockHash
        self.block[blockHash]._height = 0

        # set score to 1, since score0 means block does NOT exist. see check in storeBlockHeader()
        # this means that the score of blocks is 1 more than its calculated difficulty
        self.block[blockHash]._score = 1
        ancLen = self.numAncestorDepths
        i = 0
        while i < ancLen:
            self.block[blockHash]._ancestor[i] = blockHash
            i += 1


# store a Bitcoin block header that must be provided in
# binary format 'blockHeaderBinary'
def storeBlockHeader(blockHeaderBinary:str):
    hashPrevBlock = getBytesLE(blockHeaderBinary, 32, 4)

    if self.block[hashPrevBlock]._score == 0:  # score0 means block does NOT exist; genesis has score of 1
        return(0)

    blockHash = self.fastHashBlock(blockHeaderBinary)

    if self.block[blockHash]._score != 0:  # block already exists
        return(0)

    bits = getBytesLE(blockHeaderBinary, 4, 72)
    target = targetFromBits(bits)

    # TODO other validation of block?  eg timestamp

    if gt(blockHash, 0) && lt(blockHash, target):  #TODO should sgt and slt be used?
        self.saveAncestors(blockHash, hashPrevBlock)

        save(self.block[blockHash]._blockHeader[0], blockHeaderBinary, chars=80) # or 160?

        difficulty = 0x00000000FFFF0000000000000000000000000000000000000000000000000000 / target # https://en.bitcoin.it/wiki/Difficulty
        self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty

        if gt(self.block[blockHash]._score, self.highScore):  #TODO use sgt?
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


# return the hash of the heaviest block aka the Head
def getBlockchainHead():
    # log(self.heaviestBlock)
    return(self.heaviestBlock)


# return the score of the Head
#
# Because of setPreGenesis(), the score is 1 more than than the
# cumulative difficulty
def getChainScore():
    score = self.block[self.heaviestBlock]._score
    # log(score)
    return(score)


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
    hash1 = sha256(blockHeaderBinary:str)
    hash2 = sha256(hash1)
    res = flip32Bytes(hash2)
    return(res)


# an owner may transfer/change ownership
def setOwner(newOwner):
    if msg.sender == self.owner:
        self.owner = newOwner
        return(1)
    return(0)


#
# macros
#

# get the parent of '$blockHash'
macro getPrevBlock($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    getBytesLE($tmpStr, 32, 4)


# get the merkle root of '$blockHash'
macro getMerkleRoot($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
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
    $target = $mant * 256^($exp - 3)
    $target


# Bitcoin-way merkle parent of transaction hashes $tx1 and $tx2
macro concatHash($tx1, $tx2):
    $left = flip32Bytes($tx1)
    $right = flip32Bytes($tx2)

    $hash1 = sha256([$left, $right], chars=64)
    $hash2 = sha256($hash1)

    flip32Bytes($hash2)


# reverse 32 bytes given by '$a'
macro flip32Bytes($a):
    $o = 0
    with $i = 0:
        while $i < 32:
            mstore8(ref($o) + $i, byte(31 - $i, $a))
            $i += 1
    $o
