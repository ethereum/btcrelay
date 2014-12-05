contract BTCRelay {
  struct BlockHeader {
    Version
    hashPrevBlock
    hashMerkleRoot
    Time
    Bits
    Nonce
  }

  struct Block {
     BlockHeader header;
     uint score;
  }

  mapping (uint => Block) block;
  uint lastKnownBlock;

  function BTCRelay() {
    owner = msg.sender;

    // currently BTC block 332895 but can update later
    lastKnownBlock = '00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d';
    block[lastKnownBlock].score = 40007470271.27;
    //block[lastKnownBlock].header = ...
  }

}
