contract BTCRelay {
  struct BlockHeader {
    uint32 version;
    hash hashPrevBlock;
    hash hashMerkleRoot;
    uint32 time;
    uint32 bits;
    uint32 nonce;
  }

  hash lastKnownBlock;

  function BTCRelay() {

    // currently BTC block 332895 but can update later
    lastKnownBlock = 0x00000000000000000cfdd50d917943949fa708829ab70108c98cdb9f7d62339d;
    //block[lastKnownBlock].score = 40007470271.27;
    //block[lastKnownBlock].header = ...
  }

  function storeBlockHeader(uint32 version,
      hash hashPrevBlock,
      hash hashMerkleRoot,
      uint32 time,
      uint32 bits,
      uint32 nonce) {
    BlockHeader header;
    header.version = version;
    header.hashPrevBlock = hashPrevBlock;
    header.hashMerkleRoot = hashMerkleRoot;
    header.time = time;
    header.bits = bits;
    header.nonce = nonce;
  }

  // TODO: pass in BlockHeader when Solidity supports non-storage structs
  function isNexBlock(hash hashPrevBlock) returns (bool _) {
    if (hashPrevBlock == lastKnownBlock) {
      return true;
    }
    else {
      return false;
    }
  }
}
