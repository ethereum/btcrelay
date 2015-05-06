inset('btcChain.py')

# btcrelay can relay a transaction to any contract that has a function
# name 'processTransaction' with signature si:i
extern relayDestination: [processTransaction:si:i]


# note: _ancestor[9]
#
# a Bitcoin block (header) is stored as:
# - _blockHeader 80 bytes
# - _info who's 32 bytes are comprised of "_height" 8bytes, "_score" 16bytes, "_ibIndex" 8bytes
# -   "_height" is 1 more than the typical Bitcoin term height/blocknumber [see setPreGensesis()]
# -   "_score" is 1 more than the cumulative difficulty [see setInitialParent()]
# -   "_ibIndex" is the block's index to internalBlock (see btcChain)
# - _ancestor stores 8 32bit ancestor indices for more efficient backtracking (see btcChain)
data block[2^256](_info, _ancestor, _blockHeader[])


# block with the highest score (aka the Head of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore


macro BYTES_1: 2**8
macro BYTES_2: 2**16
macro BYTES_3: 2**24
macro BYTES_4: 2**32
macro BYTES_5: 2**40
macro BYTES_6: 2**48
macro BYTES_7: 2**56
macro BYTES_8: 2**64
macro BYTES_9: 2**72
macro BYTES_10: 2**80
macro BYTES_11: 2**88
macro BYTES_12: 2**96
macro BYTES_13: 2**104
macro BYTES_14: 2**112
macro BYTES_15: 2**120
macro BYTES_16: 2**128
macro BYTES_17: 2**136
macro BYTES_18: 2**144
macro BYTES_19: 2**152
macro BYTES_20: 2**160
macro BYTES_21: 2**168
macro BYTES_22: 2**176
macro BYTES_23: 2**184
macro BYTES_24: 2**192
macro BYTES_25: 2**200
macro BYTES_26: 2**208
macro BYTES_27: 2**216
macro BYTES_28: 2**224
macro BYTES_29: 2**232
macro BYTES_30: 2**240
macro BYTES_31: 2**248
macro BYTES_32: 2**256



# write $int64 to memory at $addrLoc
# This is useful for writing 64bit ints inside one 32 byte word
macro m_mwrite128($addrLoc, $int128):
    with $addr = $addrLoc:
        with $bytes16 = $int128:
            mstore8($addr, byte(16, $bytes16))
            mstore8($addr + 1, byte(17, $bytes16))
            mstore8($addr + 2, byte(18, $bytes16))
            mstore8($addr + 3, byte(19, $bytes16))
            mstore8($addr + 4, byte(20, $bytes16))
            mstore8($addr + 5, byte(21, $bytes16))
            mstore8($addr + 6, byte(22, $bytes16))
            mstore8($addr + 7, byte(23, $bytes16))
            mstore8($addr + 8, byte(24, $bytes16))
            mstore8($addr + 9, byte(25, $bytes16))
            mstore8($addr + 10, byte(26, $bytes16))
            mstore8($addr + 11, byte(27, $bytes16))
            mstore8($addr + 12, byte(28, $bytes16))
            mstore8($addr + 13, byte(29, $bytes16))
            mstore8($addr + 14, byte(30, $bytes16))
            mstore8($addr + 15, byte(31, $bytes16))


# write $int64 to memory at $addrLoc
# This is useful for writing 64bit ints inside one 32 byte word
macro m_mwrite64($addrLoc, $int64):
    with $addr = $addrLoc:
        with $eightBytes = $int64:
            mstore8($addr, byte(24, $eightBytes))
            mstore8($addr + 1, byte(25, $eightBytes))
            mstore8($addr + 2, byte(26, $eightBytes))
            mstore8($addr + 3, byte(27, $eightBytes))
            mstore8($addr + 4, byte(28, $eightBytes))
            mstore8($addr + 5, byte(29, $eightBytes))
            mstore8($addr + 6, byte(30, $eightBytes))
            mstore8($addr + 7, byte(31, $eightBytes))



macro m_setIbIndex($blockHash, $internalIndex):
    $word = sload(ref(self.block[$blockHash]._info))
    m_mwrite64(ref($word) + 8, $internalIndex)
    self.block[$blockHash]._info = $word


macro m_setHeight($blockHash, $blockHeight):
    $word = sload(ref(self.block[$blockHash]._info))
    m_mwrite64(ref($word), $blockHeight)
    self.block[$blockHash]._info = $word


macro m_setScore($blockHash, $blockScore):
    $word = sload(ref(self.block[$blockHash]._info))
    m_mwrite128(ref($word) + 16, $blockScore)
    self.block[$blockHash]._info = $word


macro m_getIbIndex($blockHash):
    div(sload(ref(self.block[$blockHash]._info)) * BYTES_8, BYTES_24)

macro m_getHeight($blockHash):
    div(sload(ref(self.block[$blockHash]._info)), BYTES_24)

macro m_getScore($blockHash):
    div(sload(ref(self.block[$blockHash]._info)) * BYTES_16, BYTES_16)


# def init():
    # TODO anything else to init ?
    # carefully test if adding anything to init() since
    # issues such as https://github.com/ethereum/serpent/issues/77 78 ...


#TODO for testing only; should be omitted for production
def testingonlySetHeaviest(blockHash):
    self.heaviestBlock = blockHash


# this can only be called once and allows testing of storing
# arbitrary headers and verifying/relaying transactions,
# say from block 300K, instead of Satoshi's genesis block which
# have 0 transactions until much later on
#
# This should be called using a real block on the Bitcoin blockchain.
#
# Note: If used to store the imaginary block before Satoshi's
# genesis, then it should be called as setInitialParent(0, 0, 1) and
# means that getLastBlockHeight() and getCumulativeDifficulty() will be
# 1 more than the usual: eg Satoshi's genesis has height 1 instead of 0
def setInitialParent(blockHash, height, cumulativeDifficulty):
    # reuse highScore as the flag for whether setInitialParent() has already been called
    if self.highScore != 0:
        return(0)
    else:
        self.highScore = 1  # matches the score that is set below in this function

    self.heaviestBlock = blockHash

    # _height cannot be set to -1 because inMainChain() assumes that
    # a block with height0 does NOT exist (thus we cannot allow the
    # real genesis block to be at height0)
    # self.block[blockHash]._height = height
    m_setHeight(blockHash, height)

    # do NOT pass cumulativeDifficulty of 0, since score0 means
    # block does NOT exist. see check in storeBlockHeader()
    m_setScore(blockHash, cumulativeDifficulty)

    # _ancestor can remain zeros because
    # self.internalBlock[0] already points to blockHash

    return(1)


# store a Bitcoin block header that must be provided in
# binary format 'blockHeaderBinary'
def storeBlockHeader(blockHeaderBinary:str):
    hashPrevBlock = flip32Bytes(~calldataload(40))  # 36 (header start) + 4 (offset for hashPrevBlock)

    # TODO store in var
    assert m_getScore(hashPrevBlock)  # assert prev block exists

    blockHash = m_hashBlockHeader(blockHeaderBinary)

    if m_getScore(blockHash) != 0:  # block already stored/exists
        return(0)

    bits = m_bitsFromBlockHeader()
    target = targetFromBits(bits)

    # we only check the target and do not do other validation (eg timestamp)
    # to save gas
    if blockHash > 0 && blockHash < target:
        self.saveAncestors(blockHash, hashPrevBlock)

        save(self.block[blockHash]._blockHeader[0], blockHeaderBinary, chars=80) # or 160?

        difficulty = 0x00000000FFFF0000000000000000000000000000000000000000000000000000 / target # https://en.bitcoin.it/wiki/Difficulty
        m_setScore(blockHash, m_getScore(hashPrevBlock) + difficulty)

        if m_getScore(blockHash) > self.highScore:
            self.heaviestBlock = blockHash
            self.highScore = m_getScore(blockHash)

        return(m_getHeight(blockHash))

    return(0)


# returns 1 if tx is in the block given by 'txBlockHash' and the block is
# in Bitcoin's main chain (ie not a fork)
#
# the merkle proof is represented by 'txHash', 'txIndex', 'sibling', where:
# - 'txHash' is the hash of the tx
# - 'txIndex' is the index of the tx within the block
# - 'sibling' are the merkle siblings of tx
def verifyTx(txHash, txIndex, sibling:arr, txBlockHash):
    if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
        return(0)

    merkle = self.computeMerkle(txHash, txIndex, sibling)
    realMerkleRoot = getMerkleRoot(txBlockHash)

    if merkle == realMerkleRoot:
        return(1)
    else:
        return(0)


# relays transaction to target 'contract' processTransaction() method.
# returns and logs the value of processTransaction().
#
# if the transaction does not meet verification, error code -9999
# is logged on both this contract and target contract
#
# TODO txHash can eventually be computed (dbl sha256 then flip32Bytes) when
# txStr becomes txBinary
def relayTx(txStr:str, txHash, txIndex, sibling:arr, txBlockHash, contract):
    if self.verifyTx(txHash, txIndex, sibling, txBlockHash) == 1:
        res = contract.processTransaction(txStr, txHash)
        log(msg.sender, data=[res])
        return(res)

    # log error code -9999 on both this contract and target contract
    log(msg.sender, data=[-9999])
    log(contract, data=[-9999])
    return(0)


# return the hash of the heaviest block aka the Head
def getBlockchainHead():
    # log(self.heaviestBlock)
    return(self.heaviestBlock)


# return the height of the heaviest block aka the Head
def getLastBlockHeight():
    return(m_getHeight(self.heaviestBlock))


# return the (total) cumulative difficulty of the Head
def getCumulativeDifficulty():
    cumulDifficulty = m_getScore(self.heaviestBlock)
    return(cumulDifficulty)


# return the difference between the cumulative difficulty at
# the blockchain Head and its 10th ancestor
#
# this is not needed by the relay itself, but is provided in
# case some contract wants to use the
# Bitcoin network difficulty as a data feed for some purpose
def getAverageBlockDifficulty():
    blockHash = self.heaviestBlock

    cumulDifficultyHead = m_getScore(blockHash)

    i = 0
    while i < 10:
        blockHash = getPrevBlock(blockHash)
        i += 1

    cumulDifficulty10Ancestors = m_getScore(blockHash)

    return(cumulDifficultyHead - cumulDifficulty10Ancestors)


# return -1 if there's an error (eg called with incorrect params)
# [see documentation for verifyTx() for the merkle proof
# format of 'txHash', 'txIndex', 'sibling' ]
def computeMerkle(txHash, txIndex, sibling:arr):
    resultHash = txHash
    proofLen = len(sibling)
    i = 0
    while i < proofLen:
        proofHex = sibling[i]

        sideOfSibling = txIndex % 2  # 0 means sibling is on the right; 1 means left

        if sideOfSibling == 1:
            left = proofHex
            right = resultHash
        elif sideOfSibling == 0:
            left = resultHash
            right = proofHex

        resultHash = concatHash(left, right)

        txIndex /= 2
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


#
# macros
#

# get the parent of '$blockHash'
macro getPrevBlock($blockHash):
    with $addr = ref(self.block[$blockHash]._blockHeader[0]):
        $tmp = sload($addr) * 2**32 + div(sload($addr+1), 2**224)  # must use div()
    flip32Bytes($tmp)


# get the merkle root of '$blockHash'
macro getMerkleRoot($blockHash):
    with $addr = ref(self.block[$blockHash]._blockHeader[0]):
        $tmp = sload($addr+1) * 2**32 + div(sload($addr+2), 2**224)  # must use div()
    flip32Bytes($tmp)


# Bitcoin-way of hashing a block header
macro m_hashBlockHeader($blockHeaderBytes):
    flip32Bytes(sha256(sha256($blockHeaderBytes:str)))


# get the 'bits' field from a Bitcoin blockheader
macro m_bitsFromBlockHeader():
    with $w = ~calldataload(36+72):  # 36 (header start) + 72 (offset for 'bits')
        byte(0, $w) + byte(1, $w)*256 + byte(2, $w)*TWOTO16 + byte(3, $w)*TWOTO24


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
