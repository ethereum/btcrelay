pragma solidity ^0.4.17;
contract btcrelayInterface
{

    // btcrelay can relay a transaction to any contract that has a function
    // name 'processTransaction' with signature bytes,uint256:int256
    bytes4 relayDestination = bytes4(keccak256("processTransaction(bytes,uint256) returns(int256)"));

    // block with the highest score (aka the Tip of the blockchain)
    uint256 heaviestBlock;

    //highest score among all blocks (so far)
    uint256 highScore;

    // # setInitialParent can only be called once and allows testing of storing
    // # arbitrary headers and verifying/relaying transactions,
    // # say from block 300K, instead of Satoshi's genesis block which
    // # have 0 transactions until much later on
    // #
    // # setInitialParent should be called using a real block on the Bitcoin blockchain.
    // # http://bitcoin.stackexchange.com/questions/26869/what-is-chainwork
    // # chainWork can be computed using test/script.chainwork.py or
    // # https://chainquery.com/bitcoin-api/getblock or local bitcoind
    // #
    // # Note: If used to store the imaginary block before Satoshi's
    // # genesis, then it should be called as setInitialParent(0, 0, 1) and
    // # means that getLastBlockHeight() and getChainWork() will be
    // # 1 more than the usual: eg Satoshi's genesis has height 1 instead of 0
    // # setInitialParent(0, 0, 1) is only for testing purposes and a TransactionFailed
    // # error will happen when the first block divisible by 2016 is reached, because
    // # difficulty computation requires looking up the 2016th parent, which will
    // # NOT exist with setInitialParent(0, 0, 1) (only the 2015th parent exists)
    // #
    // # To handle difficulty adjustment, in production setInitialParent should only be
    // # called with 'height such that height mod 2016 = 2015', so that
    // # TransactionFailed will be avoided when a difficulty computation is required.
    // # This means the minimum height for setInitialParent is 2015.

    function setInitialParent(bytes32 blockHash, uint256 height, uint256 chainWork) public returns(uint256);

    // # store a Bitcoin block header that must be provided in
    // # bytes format 'blockHeaderBytes'
    // # Callers must keep same signature since CALLDATALOAD is used to save gas.
    // # block header reference: https://en.bitcoin.it/wiki/Block_hashing_algorithm
    bytes4 OFFSET_ABI = 68;  // 4 bytes function ID then 2 32bytes before the header begin

    function storeBlockHeader(string blockHeaderBytes) public returns (uint256);

    // # Returns the hash of tx (raw bytes) if the tx is in the block given by 'txBlockHash'
    // # and the block is in Bitcoin's main chain (ie not a fork).
    // # Returns 0 if the tx is exactly 64 bytes long (to guard against a Merkle tree
    // # collision) or fails verification.
    // #
    // # the merkle proof is represented by 'txIndex', 'sibling', where:
    // # - 'txIndex' is the index of the tx within the block
    // # - 'sibling' are the merkle siblings of tx
    function verifyTx(bytes txBytes, int256 txIndex, int256[] sibling, int256 txBlockHash) public payable returns (uint256){}

    // # Returns 1 if txHash is in the block given by 'txBlockHash' and the block is
    // # in Bitcoin's main chain (ie not a fork)
    // # Note: no verification is performed to prevent txHash from just being an
    // # internal hash in the Merkle tree. Thus this helper method should NOT be used
    // # directly and is intended to be private.
    // #
    // # the merkle proof is represented by 'txHash', 'txIndex', 'sibling', where:
    // # - 'txHash' is the hash of the tx
    // # - 'txIndex' is the index of the tx within the block
    // # - 'sibling' are the merkle siblings of tx
    function helperVerifyHash__(
        uint256 txHash,
        uint256 txIndex,
        bytes32[] siblings,
        bytes32 txBlockHash
    ) public payable returns(uint256);

    // # relays transaction to target 'contract' processTransaction() method.
    // # returns and logs the value of processTransaction(), which is an int256.
    // #
    // # if the transaction does not pass verification, error code ERR_RELAY_VERIFY
    // # is logged and returned.
    // # Note: callers cannot be 100% certain when an ERR_RELAY_VERIFY occurs because
    // # it may also have been returned by processTransaction(). callers should be
    // # aware of the contract that they are relaying transactions to and
    // # understand what that contract's processTransaction method returns.
    //"relayTx(bytes,int256,int256[],int256,int256)"
    function relayTx(
        bytes txBytes,
        int256 txIndex,
        int256[] siblings,
        int256 txBlockHash,
        int256 contractAddress
    ) public payable returns(uint256);

    // # return the hash of the heaviest block aka the Tip
    function getBlockchainHead() returns(uint256);

    // # return the height of the heaviest block aka the Tip
    function getLastBlockHeight() returns(uint256);

    // # return the chainWork of the Tip
    // # http://bitcoin.stackexchange.com/questions/26869/what-is-chainwork
    function getChainWork() returns (uint256);

    // # return the difference between the chainWork at
    // # the blockchain Tip and its 10th ancestor
    // #
    // # this is not needed by the relay itself, but is provided in
    // # case some contract wants to use the chainWork or Bitcoin network
    // # difficulty (which can be derived) as a data feed for some purpose
    function getAverageChainWork() public returns(uint256);

    // # For a valid proof, returns the root of the Merkle tree.
    // # Otherwise the return value is meaningless if the proof is invalid.
    // # [see documentation for verifyTx() for the merkle proof
    // # format of 'txHash', 'txIndex', 'sibling' ]
    function computeMerkle(
        bytes32 txHash,
        uint256 txIndex,
        bytes32[] siblings
    ) public returns (uint256);

    // # returns true if the 'txBlockHash' is within 6 blocks of self.heaviestBlock
    // # otherwise returns false.
    // # note: return value of false does NOT mean 'txBlockHash' has more than 6
    // # confirmations; a non-existent 'txBlockHash' will lead to a return value of false
    function within6Confirmations(bytes32 txBlockHash) public returns(bool);

    // # returns the 80-byte header (zeros for a header that does not exist) when
    // # sufficient payment is provided.  If payment is insufficient, returns 1-byte of zero.
    function getBlockHeader(bytes32 blockHash) public returns(bytes32);

    // # The getBlockHash(blockHeight) method has been removed because it could be
    // # used by a leecher contract (test/btcrelay_leech.se for sample) to
    // # trustlessly provide the BTC Relay service, without rewarding the
    // # submitters of block headers, who provide a critical service.
    // # To iterate through the "blockchain" of BTC Relay, getBlockchainHead() can
    // # be used with getBlockHeader().  Once a header is obtained, its 4th byte
    // # contains the hash of the previous block, which can then be passed again
    // # to getBlockHeader().  This is how another contract can access BTC Relay's
    // # blockchain trustlessly, but each getBlockHeader() invocation potentially
    // # requires payment.
    // # As usual, UIs and eth_call with getBlockHeader() will not need any fees at all
    // # (even though sufficient 'value', by using getFeeAmount(blockHash),
    // # must still be provided).

    // # TODO is an API like getInitialParent() needed? it could be obtained using
    // # something like web3.eth.getStorageAt using index 0

    // #
    // # macros
    // # (when running tests, ensure the testing macro overrides have the
    // # same signatures as the actual macros, otherwise tests will fail with
    // # an obscure message such as tester.py:201: TransactionFailed)
    // #

    function m_difficultyShouldBeAdjusted(uint256 blockHeight) public returns(bool);

    function m_computeNewBits(
        uint256 prevTime,
        uint256 startTime,
        uint256 prevTarget
    ) public;

    // # Convert uint256 to compact encoding
    // # based on https://github.com/petertodd/python-bitcoinlib/blob/2a5dda45b557515fb12a0a18e5dd48d2f5cd13c2/bitcoin/core/serialize.py
    function m_toCompactBits(uint256 value) public;

    // get the parent of 'blockHash'
    function getPrevBlock(bytes32 blockHash) public returns(bytes32);

    //# get the timestamp from a Bitcoin blockheader
    function m_getTimestamp(bytes32 blockHash) returns(uint256);

    //# get the 'bits' field from a Bitcoin blockheader
    function m_getBits(bytes32 blockHash) public returns(bytes32);

    //# get the merkle root of '$blockHash'
    function getMerkleRoot(bytes32 blockHash) returns(bytes32);

    function m_lastBlockHeight() public returns(uint256);

    // Bitcoin-way of hashing
    function m_dblShaFlip(bytes dataBytes) public returns(bytes32);

    // # Bitcoin-way of computing the target from the 'bits' field of a blockheader
    // # based on http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
    function targetFromBits(bytes bits);

    // # Bitcoin-way merkle parent of transaction hashes $tx1 and $tx2
    function concatHash(bytes32 tx1, bytes32 tx2) returns(bytes32);

    function m_shiftRight(uint256 val, uint256 shift) returns(uint256);

    function m_shiftLeft(uint256 val, uint256 shift) returns(uint256);

    //# bit length of '$val'
    function m_bitLen(bytes val) returns(uint256);

    //# reverse 32 bytes given by '$b32'
    function flip32Bytes(bytes32 val) returns(bytes32);

    // # write $int64 to memory at $addrLoc
    // # This is useful for writing 64bit ints inside one 32 byte word
    function m_mwrite64(bytes addrLoc, bytes var64);

    // # write $int128 to memory at $addrLoc
    // # This is useful for writing 128bit ints inside one 32 byte word
    function m_mwrite128(bytes addrLoc, bytes varInt128);
    // #
    // #  macro accessors for a block's _info (height, ibIndex, score)
    // #

    //# block height is the first 8 bytes of _info
    function m_setHeight(bytes32 blockHash, uint256 blockHeight);

    function m_getHeight(bytes32 blockHash) returns(uint256);

    //# ibIndex is the index to self.internalBlock: it's the second 8 bytes of _info
    function m_setIbIndex(bytes32 blockHash, uint256 $internalIndex);

    function m_getIbIndex(bytes32 blockHash) returns (bytes32);

    //# score of the block is the last 16 bytes of _info
    function m_setScore(bytes32 blockHash, uint256 blockScore);

    function m_getScore(bytes32 blockHash) returns(uint256);

}
