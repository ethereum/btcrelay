pragma solidity ^0.4.17;
import "./constants" as constants;
contract btcChain is constants
{

    // # btcChain is required by btcrelay and is a separate file to improve
    // # clarity: it has ancestor management and its
    // # main method is inMainChain() which is tested by test_btcChain

    uint256 NUM_ANCESTOR_DEPTHS = 8;

    // # list for internal usage only that allows a 32 byte blockHash to be looked up
    // # with a 32bit int
    // # This is not designed to be used for anything else, eg it contains all block
    // # hashes and nothing can be assumed about which blocks are on the main chain
    int32[2 ^ 50] internalBlock;

    // # counter for next available slot in internalBlock
    // # 0 means no blocks stored yet and is used for the special of storing 1st block
    // # which cannot compute Bitcoin difficulty since it doesn't have the 2016th parent
    uint256 ibIndex;


    // # save the ancestors for a block, as well as updating the height
    // # note: this is internal/private so make it into a macro
    function m_saveAncestors(bytes32 blockHashArg, bytes32 hashPrevBlockArg)
    {
        bytes32 blockHash = blockHashArg;
        bytes32 hashPrevBlock = hashPrevBlockArg;
        this.internalBlock[this.ibIndex] = blockHash;
        m_setIbIndex($blockHash, this.ibIndex);
        this.ibIndex += 1;

        m_setHeight(blockHash, m_getHeight(hashPrevBlock) + 1);

        //# 8 indexes into internalBlock can be stored inside one ancestor (32 byte) word
        uint256 ancWord = 0;

        //# the first ancestor is the index to hashPrevBlock, and write it to ancWord
        uint256 prevIbIndex = m_getIbIndex(hashPrevBlock);
        m_mwrite32(ref(ancWord), prevIbIndex);

        //# update ancWord with the remaining indexes
        uint256 i = 1;
        while (i < NUM_ANCESTOR_DEPTHS)
        {
            uint256 depth = m_getAncDepth(i);
            if(m_getHeight(blockHash) % depth == 1)
            {
                m_mwrite32(ref(ancWord) + 4 * i, prevIbIndex);
            }
            else
            {
                m_mwrite32(ref(ancWord) + 4 * i, m_getAncestor(hashPrevBlock, i));
            }
            i++;

            uint256 depth = m_getAncDepth(i);

            if (m_getHeight($blockHash) % $depth == 1)
            {
                m_mwrite32(ref($ancWord) + 4* i,  prevIbIndex);
            }
            else
            {
                m_mwrite32(ref($ancWord) + 4 * i, m_getAncestor( hashPrevBlock,  i));
            }
            i++;

            //# write the ancestor word to storage
            this.block[blockHash]._ancestor = ancWord;
        }
    }

    // # private (to prevent leeching)
    // # returns 1 if 'txBlockHash' is in the main chain, ie not a fork
    // # otherwise returns 0
    function priv_inMainChain__(bytes32 txBlockHash) private returns(bool)
    {
        require(msg.sender == this);
        uint256 txBlockHash = m_getHeight(txBlockHash);
        // # By assuming that a block with height 0 does not exist, we can do
        // # this optimization and immediate say that txBlockHash is not in the main chain.
        // # However, the consequence is that
        // # the genesis block must be at height 1 instead of 0 [see setInitialParent()]
        if(txBlockHash == 0) return 0;
        return this.priv_fastGetBlockHash__(txBlockHeight) == txBlockHash;
    }


    // # private (to prevent leeching)
    // # callers must ensure 2 things:
    // # * blockHeight is greater than 0 (otherwise infinite loop since
    // # minimum height is 1)
    // # * blockHeight is less than the height of heaviestBlock, otherwise the
    // # heaviestBlock is returned
    function priv_fastGetBlockHash__(uint256 blockHeight) returns(bytes32)
    {
        require(msg.sender == this);
        bytes32 blockHash = this.heaviestBlock;
        uint256 anc_index = NUM_ANCESTOR_DEPTHS - 1;
        while(m_getHeight(blockHash) > blockHeight)
        {
            while(m_getHeight(blockHash) - blockHeight < m_getAncDepth(anc_index)
            && anc_index > 0)
            {
                anc_index--;
            }
            blockHash = this.internalBlock[m_getAncestor(blockHash, anc_index)];
        }
        return blockHash;
    }

    // #
    // # macros
    // #


    // # a block's _ancestor storage slot contains 8 indexes into internalBlock, so
    // # this macro returns the index that can be used to lookup the desired ancestor
    // # eg. for combined usage, self.internalBlock[m_getAncestor(someBlock, 2)] will
    // # return the block hash of someBlock's 3rd ancestor
    function m_getAncestor(bytes32 blockHash, uint256 whichAncestor) returns(uint256)
    {
        return div(sload(this.bitcoinBlock[blockHash]._ancestor * 2 ** (32 * whichAncestor)), BYTES_28);
    }


    //# index should be 0 to 7, so this returns 1, 5, 25 ... 78125
    function m_getAncDepth(uint256 index) returns(uint256)
    {
        return 5 ** index;
    }

    // # write $int32 to memory at $addrLoc
    // # This is useful for writing 32bit ints inside one 32 byte word
    function m_mwrite32(int32 addrLoc, int32 int32Var)
    {
        int32 addr = addrLoc;
        int32 fourBytes = int32Var;
        //assembly {
            mstore8(addr, byte(28, fourBytes));
            mstore8(addr + 1, byte(29, fourBytes));
            mstore8(addr + 2, byte(30, fourBytes));
            mstore8(addr + 3, byte(31, fourBytes));
        //}
    }

    // # write $int24 to memory at $addrLoc
    // # This is useful for writing 24bit ints inside one 32 byte word
    function m_mwrite24(int24 addrLoc, int24 varInt24)
    {
        int24 addr = addrLoc;
        int24 threeBytes = varInt24;
        //assembly {
            mstore8($addr, byte(29, $threeBytes));
            mstore8($addr + 1, byte(30, $threeBytes));
            mstore8($addr + 2, byte(31, $threeBytes));
        //}
    }


    // # write $int16 to memory at $addrLoc
    // # This is useful for writing 16bit ints inside one 32 byte word
    function m_mwrite16(int16 addrLoc, int16 varInt16)
    {
        int16 addr = addrLoc;
        int16 twoBytes = varInt16;
        // assembly
        // {
            mstore8($addr, byte(30, $twoBytes));
            mstore8($addr + 1, byte(31, $twoBytes));
        //}
    }

}
