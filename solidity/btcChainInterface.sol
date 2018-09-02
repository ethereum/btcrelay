pragma solidity ^0.4.17;
contract btcChainInterface
{

    function m_saveAncestors(bytes32 blockHashArg, bytes32 hashPrevBlockArg);

    // # private (to prevent leeching)
    // # returns 1 if 'txBlockHash' is in the main chain, ie not a fork
    // # otherwise returns 0
    function priv_inMainChain__(bytes32 txBlockHash) private returns(bool);


    // # private (to prevent leeching)
    // # callers must ensure 2 things:
    // # * blockHeight is greater than 0 (otherwise infinite loop since
    // # minimum height is 1)
    // # * blockHeight is less than the height of heaviestBlock, otherwise the
    // # heaviestBlock is returned
    function priv_fastGetBlockHash__(uint256 blockHeight) returns(bytes32);

    // #
    // # macros
    // #


    // # a block's _ancestor storage slot contains 8 indexes into internalBlock, so
    // # this macro returns the index that can be used to lookup the desired ancestor
    // # eg. for combined usage, self.internalBlock[m_getAncestor(someBlock, 2)] will
    // # return the block hash of someBlock's 3rd ancestor
    function m_getAncestor(bytes32 blockHash, uint256 whichAncestor) returns(uint256);

    //# index should be 0 to 7, so this returns 1, 5, 25 ... 78125
    function m_getAncDepth(uint256 index) returns(uint256);

    // # write $int32 to memory at $addrLoc
    // # This is useful for writing 32bit ints inside one 32 byte word
    function m_mwrite32(int32 addrLoc, int32 int32Var);

    // # write $int24 to memory at $addrLoc
    // # This is useful for writing 24bit ints inside one 32 byte word
    function m_mwrite24(int24 addrLoc, int24 varInt24);

    // # write $int16 to memory at $addrLoc
    // # This is useful for writing 16bit ints inside one 32 byte word
    function m_mwrite16(int16 addrLoc, int16 varInt16);

}
