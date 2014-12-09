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

  function flipBytes(uint n) {
    uint mask = 0xff;
    var b1 = n & mask;
    b1 *= 2^(31*8);
    mask *= 256;

    var b2 = n & mask;  // no arrays in Solidity yet
    b2 /= 2^8;
    b2 *= 2^(30*8);
    mask *= 256;

    var b3 = n & mask;
    b3 /= 2^(2*8);
    b3 *= 2^(29*8);
    mask *= 256;

    var b4 = n & mask;
    b4 /= 2^(3*8);
    b4 *= 2^(28*8);
    mask *= 256;

    var b5 = n & mask;
    b5 /= 2^(4*8);
    b5 *= 2^(27*8);
    mask *= 256;

    var b6 = n & mask;
    b6 /= 2^(5*8);
    b6 *= 2^(26*8);
    mask *= 256;

    var b7 = n & mask;
    b7 /= 2^(6*8);
    b7 *= 2^(25*8);
    mask *= 256;

    var b8 = n & mask;
    b8 /= 2^(7*8);
    b8 *= 2^(24*8);
    mask *= 256;

    var b9 = n & mask;
    b9 /= 2^(8*8);
    b9 *= 2^(23*8);
    mask *= 256;

    var b10 = n & mask;
    b10 /= 2^(7*8);
    b10 *= 2^(24*8);
    mask *= 256;

    var b11 = n & mask;
    mask *= 256;
/*    var b12 = n & mask;
    mask *= 256;
    var b13 = n & mask;
    mask *= 256;
    var b14 = n & mask;
    mask *= 256;
    var b15 = n & mask;
    mask *= 256;
    var b16 = n & mask;
    mask *= 256;
    var b17 = n & mask;
    mask *= 256;
    var b18 = n & mask;
    mask *= 256;
    var b19 = n & mask;
    mask *= 256;
    var b20 = n & mask;
    mask *= 256;
    var b21 = n & mask;
    mask *= 256;
    var b22 = n & mask;
    mask *= 256;
    var b23 = n & mask;
    mask *= 256;
    var b24 = n & mask;
    mask *= 256;
    var b25 = n & mask;
    mask *= 256;
    var b26 = n & mask;
    mask *= 256;
    var b27 = n & mask;
    mask *= 256;
    var b28 = n & mask;
    mask *= 256;
    var b29 = n & mask;
    mask *= 256;
    var b30 = n & mask;
    mask *= 256;
    var b31 = n & mask;
    mask *= 256;
    var b32 = n & mask;
*/
    //return b1 | b2 | b3 | b4 | b5 |
  }

  function slt(uint n, uint x) returns (uint _) {
    return n * (2^x);
  }
}
