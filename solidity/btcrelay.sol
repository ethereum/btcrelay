pragma solidity ^0.4.17;
import "./incentive" as incentive;
import "./btcChain" as btcChain;
contract btcrelay is incentive, btcChain
{

    // btcrelay can relay a transaction to any contract that has a function
    // name 'processTransaction' with signature bytes,uint256:int256
    bytes4 relayDestination = bytes4(keccak256("processTransaction(bytes,uint256) returns(int256)"));

    // a Bitcoin block (header) is stored as:
    // - _blockHeader 80 bytes
    // - _info who's 32 bytes are comprised of "_height" 8bytes, "_ibIndex" 8bytes, "_score" 16bytes
    // -   "_height" is 1 more than the typical Bitcoin term height/blocknumber [see setInitialParent()]
    // -   "_ibIndex" is the block's index to internalBlock (see btcChain)
    // -   "_score" is 1 more than the chainWork [see setInitialParent()]
    // - _ancestor stores 8 32bit ancestor indices for more efficient backtracking (see btcChain)
    // - _feeInfo is used for incentive.se (see m_getFeeInfo)
    struct bitcoinBlock
    {
        bytes32 _info;
        bytes32 _ancestor;
        bytes[] _blockHeader;
        bytes32 _feeInfo;
    }

    // block with the highest score (aka the Tip of the blockchain)
    uint256 heaviestBlock;

    //highest score among all blocks (so far)
    uint256 highScore;

    event StoreHeader(uint256 indexed blockHash, int256 indexed returnCode);
    event GetHeader(uint256 indexed blockHash, int256 indexed returnCode);
    event VerifyTransaction(uint256 indexed txHash, int256 indexed returnCode);
    event RelayTransaction(uint256 indexed txHash, int256 indexed returnCode);

    constructor() public
    {
        // gasPriceAndChangeRecipientFee in incentive.se
        incentive.gasPriceAndChangeRecipientFee = bytes16(50 * 10**9); // 50 shannon and left-align
        // carefully test if adding anything to init() since
        // issues such as https://github.com/ethereum/serpent/issues/77 78 ...
    }

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

    function setInitialParent(bytes32 blockHash, uint256 height, uint256 chainWork) public returns(uint256)
    {
        //reuse highScore as the flag for whether setInitialParent() has already been called
        if(highScore != 0)
        {
            return 0;
        }
        else
        {
            return highScore = 1;
        }
        heaviestBlock = blockHash;
        // # _height cannot be set to -1 because inMainChain() assumes that
        // # a block with height0 does NOT exist (thus we cannot allow the
        // # real genesis block to be at height0)
        m_setHeight(blockHash, height);
        // # do NOT pass chainWork of 0, since score0 means
        // # block does NOT exist. see check in storeBlockHeader()
        m_setScore(blockHash, chainWork);
        // # other fields do not need to be set, for example:
        // # _ancestor can remain zeros because self.internalBlock[0] already points to blockHash
        return 1;
    }

    // # store a Bitcoin block header that must be provided in
    // # bytes format 'blockHeaderBytes'
    // # Callers must keep same signature since CALLDATALOAD is used to save gas.
    // # block header reference: https://en.bitcoin.it/wiki/Block_hashing_algorithm
    bytes4 OFFSET_ABI = 68;  // 4 bytes function ID then 2 32bytes before the header begin

    function storeBlockHeader(string blockHeaderBytes) public returns (uint256)
    {
        bytes32 hashPrevBlock = flip32Bytes(calldataload(OFFSET_ABI + 4));
        blockHash = m_dblShaFlip(blockHeaderBytes);

        uint256 scorePrevBlock = m_getScore(hashPrevBlock);
        if (scorePrevBlock == 0)
        {
            return 0;
        }

        uint256 scoreBlock = m_getScore(hashPrevBlock);
        if(scoreBlock != 0) // block already stored/exists
        {
            return 0;
        }

        bytes32 wordWithBits = calldataload(OFFSET_ABI + 72); // 72 is offset for 'bits'
        bytes bits = byte(0, wordWithBits)
        + byte(1, wordWithBits)
        + byte(2, wordWithBits)
        + byte(3, wordWithBits);

        bytes target = targetFromBits(bits);

        // we only check the target and do not do other validation (eg timestamp) to save gas
        if(blockHash > 0 && blockHash < target)
        {
            uint256 blockHeight = 1 + m_getHeight(hashPrevBlock);
            bytes prevBits = m_getBits(hashPrevBlock);
            if(!m_difficultyShouldBeAdjusted(blockHeight) || _ibIndex == 1)
            {
                // # since blockHeight is 1 more than blockNumber; OR clause is special case for 1st header
                // # we need to check prevBits isn't 0 otherwise the 1st header
                // # will always be rejected (since prevBits doesn't exist for the initial parent)
                // # This allows blocks with arbitrary difficulty from being added to
                // # the initial parent, but as these forks will have lower score than
                // # the main chain, they will not have impact.
                if(bits != prevBits && prevBits != 0)
                {
                    //TODO handle logs
                    return 0;
                }
            }
            else
            {
                uint256 prevTarget = targetFromBits(prevBits);
                uint256 prevTime = m_getTimestamp(hashPrevBlock);
                // (blockHeight - DIFFICULTY_ADJUSTMENT_INTERVAL) is same as [getHeight(hashPrevBlock) - (DIFFICULTY_ADJUSTMENT_INTERVAL - 1)]
                uint256 startBlock = priv_fastGetBlockHash__(blockHeight - DIFFICULTY_ADJUSTMENT_INTERVAL);
                uint256 startTime = m_getTimestamp(startBlock);

                bytes newBits = m_computeNewBits(prevTime, startTime, prevTarget);
                if(bits != newBits && newBits != 0) // newBits != 0 to allow first header
                {
                    return 0;
                }
            }
            m_saveAncestors(blockHash, hashPrevBlock); // increments _ibIndex

            save(bitcoinBlock[blockHash]._blockHeader[0], blockHeaderBytes, 80);
            uint256 difficulty = 0x00000000FFFF0000000000000000000000000000000000000000000000000000 / target; //# https://en.bitcoin.it/wiki/Difficulty
            scoreBlock = scorePrevBlock + difficulty;
            m_setScore(blockHash, scoreBlock);
            // # equality allows block with same score to become an (alternate) Tip, so that
            // # when an (existing) Tip becomes stale, the chain can continue with the alternate Tip
            if(scoreBlock >= highScore)
            {
                heaviestBlock = blockHash;
                highScore = scoreBlock;
            }
            return blockHeight;
        }

        return 0;

    }

    // # Returns the hash of tx (raw bytes) if the tx is in the block given by 'txBlockHash'
    // # and the block is in Bitcoin's main chain (ie not a fork).
    // # Returns 0 if the tx is exactly 64 bytes long (to guard against a Merkle tree
    // # collision) or fails verification.
    // #
    // # the merkle proof is represented by 'txIndex', 'sibling', where:
    // # - 'txIndex' is the index of the tx within the block
    // # - 'sibling' are the merkle siblings of tx
    function verifyTx(
        bytes txBytes,
        uint256 txIndex,
        bytes32[] sibling,
        uint256 txBlockHash
    ) public payable returns (uint256)
    {
        bytes32 txHash = m_dblShaFlip(txBytes);
        if(txBytes.length == 64) //TODO - is check 32 also needed?
        {
            return 0;
        }
        uint256 res = helperVerifyHash__(txHash, txIndex, sibling, txBlockHash, msg.value);
        if (res == 1)
        {
            return txHash;
        }
        else
        {
            return 0;
        }
    }

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
    ) public payable returns(uint256)
    {
        bool feePaid = feePaid(txBlockHash, m_getFeeAmount(txBlockHash), msg.value);
        if (!feePaid)
        {
            return ERR_BAD_FEE;
        }
        if (within6Confirmations(txBlockHash))
        {
            return ERR_CONFIRMATIONS;
        }

        bytes32 merkle = computeMerkle(txHash, txIndex, siblings);
        realMerkleRoot = getMerkleRoot(txBlockHash);

        if(merkle == realMerkleRoot)
        {
            return 1;
        }

        return ERR_MERKLE_ROOT;
    }

    // # relays transaction to target 'contract' processTransaction() method.
    // # returns and logs the value of processTransaction(), which is an int256.
    // #
    // # if the transaction does not pass verification, error code ERR_RELAY_VERIFY
    // # is logged and returned.
    // # Note: callers cannot be 100% certain when an ERR_RELAY_VERIFY occurs because
    // # it may also have been returned by processTransaction(). callers should be
    // # aware of the contract that they are relaying transactions to and
    // # understand what that contract's processTransaction method returns.
    function relayTx(
        bytes32 txBytes,
        bytes32[] siblings,
        bytes32 txBlockHash,
        address contractAddress
    ) public payable returns(uint256)
    {
        uint256 txHash = verifyTx(txBytes, txIndex, siblings, txBlockHash, msg.value);
        if(txHash != 0)
        {
            return contractAddress.processTransaction(txBytes, txHash);
        }
        return ERR_RELAY_VERIFY;
    }

    // # return the hash of the heaviest block aka the Tip
    function getBlockchainHead() returns(uint256)
    {
        return heaviestBlock;
    }

    // # return the height of the heaviest block aka the Tip
    function getLastBlockHeight() returns(uint256)
    {
        return m_lastBlockHeight();
    }

    // # return the chainWork of the Tip
    // # http://bitcoin.stackexchange.com/questions/26869/what-is-chainwork
    function getChainWork() returns (uint256)
    {
        return m_getScore(heaviestBlock);
    }

    // # return the difference between the chainWork at
    // # the blockchain Tip and its 10th ancestor
    // #
    // # this is not needed by the relay itself, but is provided in
    // # case some contract wants to use the chainWork or Bitcoin network
    // # difficulty (which can be derived) as a data feed for some purpose
    function getAverageChainWork() public returns(uint256)
    {
        uint256 blockHash = heaviestBlock;
        uint256 chainWorkTip = m_getScore(blockHash);
        uint i = 0;
        while (i < 10)
        {
            blockHash = getPrevBlock(blockHash);
            i++;
        }
        uint256 chainWork10Ancestors = m_getScoreZ(blockHash);
        return chainWorkTip - chainWork10Ancestors;
    }

    // # For a valid proof, returns the root of the Merkle tree.
    // # Otherwise the return value is meaningless if the proof is invalid.
    // # [see documentation for verifyTx() for the merkle proof
    // # format of 'txHash', 'txIndex', 'sibling' ]
    function computeMerkle(
        bytes32 txHash,
        uint256 txIndex,
        bytes32[] siblings
    ) public returns (uint256)
    {
        bytes32 resultHash = txHash;
        uint256 proofLength = siblings.length;
        uint i = 0;
        while(i < proofLength)
        {
            bytes32 proofHex = siblings[i];
            uint256 sideOfSibling = txIndex % 2; // # 0 means sibling is on the right; 1 means left
            bytes32 left;
            bytes32 right;
            if(sideOfSibling == 1)
            {
                left = proofHex;
                right = resultHash;
            }
            else if(sideOfSibling == 0)
            {
                left = resultHash;
                right = proofHex;
            }

            resultHash = concatHash(left, right);
            txIndex /= 2;
            i++;
        }
        return resultHash;
    }

    // # returns true if the 'txBlockHash' is within 6 blocks of self.heaviestBlock
    // # otherwise returns false.
    // # note: return value of false does NOT mean 'txBlockHash' has more than 6
    // # confirmations; a non-existent 'txBlockHash' will lead to a return value of false
    function within6Confirmations(bytes32 txBlockHash) public returns(bool)
    {
        bytes32 blockHash = heaviestBlock;
        uint256 i = 0;
        while (i < 6)
        {
            if(txBlockHash == blockHash)
            {
                return true;
            }
            // # blockHash = self.block[blockHash]._prevBlock
            bytes32 blockHash = getPrevBlock(blockHash);
            i++;
        }
        return false;
    }

    // # returns the 80-byte header (zeros for a header that does not exist) when
    // # sufficient payment is provided.  If payment is insufficient, returns 1-byte of zero.
    function getBlockHeader(bytes32 blockHash) public returns(bytes32)
    {
        if (!feePaid(blockHash, m_getFeeAmount(blockHash), msg.value))
        {
            return bytes32("\x00");
        }
        return load(bitcoinBlock[blockHash]._blockHeader[0], 80);
    }

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

    function m_difficultyShouldBeAdjusted(uint256 blockHeight) public returns(bool)
    {
        return mod(blockHeight, DIFFICULTY_ADJUSTMENT_INTERVAL) == 0;
    }

    function m_computeNewBits(
        uint256 prevTime,
        uint256 startTime,
        uint256 prevTarget
    ) public
    {
        uint256 actualTimeSpan = prevTime - startTime;
        if(actualTimeSpan < TARGET_TIMESPAN_DIV_4)
        {
            actualTimeSpan = TARGET_TIMESPAN_DIV_4;
        }
        if(actualTimeSpan > TARGET_TIMESPAN_MUL_4)
        {
            actualTimeSpan = TARGET_TIMESPAN_MUL_4;
        }
        uint256 newTarget = div(actualTimeSpan * prevTarget, TARGET_TIMESPAN);
        if(newTarget > UNROUNDED_MAX_TARGET)
        {
            newTarget = UNROUNDED_MAX_TARGET;
        }
        m_toCompactBits(newTarget);
    }

    // # Convert uint256 to compact encoding
    // # based on https://github.com/petertodd/python-bitcoinlib/blob/2a5dda45b557515fb12a0a18e5dd48d2f5cd13c2/bitcoin/core/serialize.py
    function m_toCompactBits(uint256 value) public
    {
        uint256 nbytes = m_shiftRight((m_bitLen(val) + 7), 3);
        uint256 compact = 0;
        if (nbytes <= 3)
        {
            compact = m_shiftLeft((value & 0xFFFFFF), 8 * (3 - nbytes));
        }
        else
        {
            compact = m_shiftRight(value, 8 * (nbytes - 3));
            compact = compact & 0xFFFFFF;
        }
        // # If the sign bit (0x00800000) is set, divide the mantissa by 256 and
        // # increase the exponent to get an encoding without it set.
        if(compact & 0x00800000)
        {
            compact = m_shiftRight(compact, 8);
        }

        compact | m_shiftRight(nbytes, 24);

    }

    // get the parent of 'blockHash'
    function getPrevBlock(bytes32 blockHash) public returns(bytes32)
    {
        address addr = ref(bitcoinBlock[blockHash]._blockHeader[0]);
        // # sload($addr) gets first 32bytes
        // # * BYTES_4 shifts over to skip the 4bytes of blockversion
        // # At this point we have the first 28bytes of hashPrevBlock and we
        // # want to get the remaining 4bytes so we:
        // # sload($addr+1) get the second 32bytes
        // #     but we only want the first 4bytes so div 28bytes
        // # The single line statement can be interpreted as:
        // # get the last 28bytes of the 1st chunk and combine (add) it to the
        // # first 4bytes of the 2nd chunk,
        // # where chunks are read in sizes of 32bytes via sload
        return flip32Bytes(sload($addr) * BYTES_4 + div(sload($addr+1), BYTES_28)); // # must use div()
    }

    //# get the timestamp from a Bitcoin blockheader
    function m_getTimestamp(bytes32 blockHash) returns(uint256)
    {
        uint256 addr = uint256(bitcoinBlock[blockHash]._blockHeader[0]) + 2;
        // get the 3rd chunk
        assembly {
            let tmp := sload(addr)
        }
        bytes32 timestamp = bytes3(byte(7, tmp)) + bytes2(6, tmp) +  bytes1(5, tmp) +byte(4, tmp);
        return uint256(timestamp);
    }

    //# get the 'bits' field from a Bitcoin blockheader
    function m_getBits(bytes32 blockHash) public returns(bytes32)
    {
        uint256 addr = uint256(bitcoinBlock[blockHash]._blockHeader[0]) + 2;
        // get the 3rd chunk
        assembly {
            let tmp := sload(addr)
        }
        bytes32 bits = bytes3(byte(7, tmp)) + bytes2(6, tmp) +  bytes1(5, tmp) + byte(4, tmp);
        return bits;
    }

    //# get the merkle root of '$blockHash'
    function getMerkleRoot(bytes32 blockHash) returns(bytes32)
    {
        uint256 addr = uint256(bitcoinBlock[blockHash]._blockHeader[0]) + 2;
        return flip32Bytes(bytes4(addr + 1), div(bytes28(addr + 2)));
    }

    function m_lastBlockHeight() public returns(uint256)
    {
        return m_getHeight(heaviestBlock);
    }

    // Bitcoin-way of hashing
    function m_dblShaFlip(bytes dataBytes) public returns(bytes32)
    {
        return flip32Bytes(sha256(sha256(dataBytes)));
    }

    // # Bitcoin-way of computing the target from the 'bits' field of a blockheader
    // # based on http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
    function targetFromBits(bytes bits)
    {
        uint256 exp = div(bits, 0x1000000); // 2 & 24
        uint256 mant = bits & 0xffffff;
        mant = 256^(exp - 3);
    }

    // # Bitcoin-way merkle parent of transaction hashes $tx1 and $tx2
    function concatHash(bytes32 tx1, bytes32 tx2) returns(bytes32)
    {
        assembly
        {
            let x := alloc(64)
            mstore(alloc(64), flip32Bytes(tx1))
            mstore(alloc(64) + 32, flip32Bytes(tx2))
            return flip32Bytes(sha256(sha256(alloc(64), 64)))
        }
    }

    function m_shiftRight(uint256 val, uint256 shift) returns(uint256)
    {
        return div(val, 2**shift);
    }

    function m_shiftLeft(uint256 val, uint256 shift) returns(uint256)
    {
        return val * 2**shift;
    }

    //# bit length of '$val'
    function m_bitLen(bytes val) returns(uint256)
    {
        return val.length * 8;
    }

    //# reverse 32 bytes given by '$b32'
    function flip32Bytes(bytes32 val) returns(bytes32)
    {
        bytes32 b32 = val;
        uint256 i = 0;
        while (i < 32) {
            // # unrolling this would decrease gas usage, but would increase
            // # the gas cost for code size by over 700K and exceed the PI million block gas limit
            assembly {
                mstore8(ref(b32) + i, byte(31 - i, a));
            }
            i++;
        }
        return b32;
    }

    // # write $int64 to memory at $addrLoc
    // # This is useful for writing 64bit ints inside one 32 byte word
    function m_mwrite64(bytes addrLoc, bytes var64)
    {
        bytes  addr = addrLoc;
        bytes8 eightBytes = var64;
        assembly {
            mstore8(addr, byte(24, eightBytes))
            mstore8(addr + 1, byte(25, eightBytes))
            mstore8(addr + 2, byte(26, eightBytes))
            mstore8(addr + 3, byte(27, eightBytes))
            mstore8(addr + 4, byte(28, eightBytes))
            mstore8(addr + 5, byte(29, eightBytes))
            mstore8(addr + 6, byte(30, eightBytes))
            mstore8(addr + 7, byte(31, eightBytes))
        }
    }

    // # write $int128 to memory at $addrLoc
    // # This is useful for writing 128bit ints inside one 32 byte word
    function m_mwrite128(bytes addrLoc, bytes varInt128)
    {
        bytes  addr = addrLoc;
        bytes16 sixteenBytes = varInt128;
        assembly {
            mstore8($addr, byte(16, sixteenBytes))
            mstore8($addr + 1, byte(17, sixteenBytes))
            mstore8($addr + 2, byte(18, sixteenBytes))
            mstore8($addr + 3, byte(19, sixteenBytes))
            mstore8($addr + 4, byte(20, sixteenBytes))
            mstore8($addr + 5, byte(21, sixteenBytes))
            mstore8($addr + 6, byte(22, sixteenBytes))
            mstore8($addr + 7, byte(23, sixteenBytes))
            mstore8($addr + 8, byte(24, sixteenBytes))
            mstore8($addr + 9, byte(25, sixteenBytes))
            mstore8($addr + 10, byte(26, sixteenBytes))
            mstore8($addr + 11, byte(27, sixteenBytes))
            mstore8($addr + 12, byte(28, sixteenBytes))
            mstore8($addr + 13, byte(29, sixteenBytes))
            mstore8($addr + 14, byte(30, sixteenBytes))
            mstore8($addr + 15, byte(31, sixteenBytes))
        }
    }

    // #
    // #  macro accessors for a block's _info (height, ibIndex, score)
    // #

    //# block height is the first 8 bytes of _info
    function m_setHeight(bytes32 blockHash, uint256 blockHeight)
    {
        assembly {
            let word = sload(ref(bitcoinBlock[blockHash]._info))
            m_mwrite64(ref(word), blockHeight)
            bitcoinBlock[blockHash]._info = word
        }
    }

    function m_getHeight(bytes32 blockHash) returns(uint256)
    {
        assembly {
            div(sload(ref(bitcoinBlock[blockHash._info])), BYTES_24)
        }
    }

    //# ibIndex is the index to self.internalBlock: it's the second 8 bytes of _info
    function m_setIbIndex(bytes32 blockHash, uint256 $internalIndex)
    {
        assembly {
            let word = sload(ref(bitcoinBlock[blockHash]._info))
            m_mwrite64(ref(word) + 8, $internalIndex)
            // this?
            this.bitcoinBlock[blockHash]._info = word
        }
    }

    function m_getIbIndex(bytes32 blockHash) returns (bytes32) {
        assembly {
            return div(sload(ref(bitcoinBlock[blockHash]._info * BYTES_8, BYTES_24)))
        }
    }

    //# score of the block is the last 16 bytes of _info
    function m_setScore(bytes32 blockHash, uint256 blockScore)
    {
        assembly {
            let word = sload(ref(this.bitcoinBlock[blockHash]._info))
            m_mwrite128(ref(word) + 26, blockScore)
            this.block[blockHash]._info = word
        }
    }

    function m_getScore(bytes32 blockHash) returns(uint256)
    {
        assembly {
            return div(sload(ref(this.bitcoinBlock[blockHash._info])) * BYTES_16, BYTES_16)
        }
    }

}
