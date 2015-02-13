inset('btczzz.py')

# test macro doRawHashBlockHeader
def testDoRawHashBlockHeader():
    # https://en.bitcoin.it/wiki/Block_hashing_algorithm
    version = 0x01000000
    hashPrevBlock = 0x81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000
    hashMerkleRoot = 0xe320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b
    time = 0xc7f5d74d
    bits = 0xf2b9441a
    nonce = 0x42a14695

    # these should be the intermediate b1,b2,b3 values inside doRawHashBlockHeader()
    # b1 = 0x0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    # b2 = 0x00000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    # b3 = 0xf1fc122bc7f5d74df2b9441a42a1469500000000000000000000000000000000
    # hash1 = sha256([b1,b2,b3], chars=80)
    # hash2 = sha256([hash1], 1)
    # return(hash2)

    res = doRawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    # log(res)

    expHash = 0x1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000
    return(res == expHash)


def testHashHeader():
    version = 2
    hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
    time = 1417792088
    bits = 0x181b7b74
    nonce = 796195988

    expBlockHash = 0x000000000000000010e318d0c61da0b84246481d9cc097fda9327fe90b1538c1
    blockHash = hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(blockHash == expBlockHash)
