contract BTCRelay {
  uint TWO_POW_24;

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
    TWO_POW_24 = 2 ^ 24;

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

    var exp = bits / TWO_POW_24; // is SDIV needed or this is already equivalent to bits >> 24;
    var mant = bits & 0xffffff;
    var target = (mant * slt(1, (8*(exp - 3))));
    //target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    //target_str = target_hexstr.decode('hex')

    //header = ( struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
          //mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time_, bits, nonce))
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

  function slt(uint n, uint x) returns (uint _) {
    return n * (2^x);
  }
}
