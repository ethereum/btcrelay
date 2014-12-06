contract BTCRelay {
  struct BlockHeader {
    uint32 version;
    uint hashPrevBlock;
    uint hashMerkleRoot;
    uint32 time;
    uint32 bits;
    uint32 nonce;
  }

  uint lastKnownBlock;

  function BTCRelay() {

    // currently BTC block 332895 but can update later
    lastKnownBlock = 0x00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d;
    //block[lastKnownBlock].score = 40007470271.27;
    //block[lastKnownBlock].header = ...
  }

}
