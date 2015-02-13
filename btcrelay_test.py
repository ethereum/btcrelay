inset('btcrelay.py')

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

def testTargetFromBits():
    bits = 0x19015f53
    exp = 8614444778121073626993210829679478604092861119379437256704
    res = targetFromBits(bits)
    return(res == exp)


def testConcatHash():
    tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    r = concatHash(tx1, tx2)
    return(r == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815)


# this will need fixing.  for ideas see test/test_btcTx.py
def testRelayTx():
    # this is duped from testVerifyTx since there seems to be issues with accessing arrays
    # returned by a function (see setupProof branch)

    b0 = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
    b1 = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090 # block #100001
    b2 = 0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
    b3 = 0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1
    b4 = 0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79
    b5 = 0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45
    b6 = 0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60

    self.heaviestBlock = b6

    self.block[b6]._blockHeader._prevBlock = b5
    self.block[b5]._blockHeader._prevBlock = b4
    self.block[b4]._blockHeader._prevBlock = b3
    self.block[b3]._blockHeader._prevBlock = b2
    self.block[b2]._blockHeader._prevBlock = b1
    self.block[b1]._blockHeader._prevBlock = b0

    self.block[b0]._blockHeader._mrklRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766

    # values are from block 100K
    tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    proofLen = 2
    hash = array(proofLen)
    path = array(proofLen)

    hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    path[0] = RIGHT_HASH

    hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
    path[1] = RIGHT_HASH

    txBlockHash = b0
    BTC_ETH = create('btc-eth.py')
    res = self.relayTx(tx, proofLen, hash, path, txBlockHash, BTC_ETH)
    return(res)
    # expB0 = 1 == self.relayTx(tx, proofLen, hash, path, txBlockHash)
    # return(-1)
