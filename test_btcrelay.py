

def runTests():
    ALL_GOOD = 99999
    i = 100
    if self.testIsNonceValid() != 1:
        return(i)
    i += 1

    if self.test__rawHashBlockHeader() != 1:
        return(i)
    i += 1

    if self.testHashHeader() != 1:
        return(i)
    i += 1

    if self.testStoreBlockHeader() != 1:
        return(i)
    i += 1

    if self.testConcatHash() != 1:
        return(i)
    i += 1

    if self.testWithin6Confirms() != 1:
        return(i)
    i += 1

    if self.testComputeMerkle() != 1:
        return(i)
    i += 1

    if self.testVerifyTx() != 1:
        return(i)
    i += 1

    return(ALL_GOOD)


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

def testVerifyTx():
    # verifyTx should only return 1 for b0
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

    txBlockHash = 0xdead
    expFake = 0 == self.verifyTx(tx, proofLen, hash, path, txBlockHash)

    txBlockHash = b1
    expB1 = 0 == self.verifyTx(tx, proofLen, hash, path, txBlockHash)

    # verifyTx should only return 1 for b0
    txBlockHash = b0
    expB0 = 1 == self.verifyTx(tx, proofLen, hash, path, txBlockHash)

    return(expFake and expB1 and expB0)

def testComputeMerkle():
    # values are from block 100K
    tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    proofLen = 2
    hash = array(proofLen)
    path = array(proofLen)

    hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    path[0] = RIGHT_HASH

    hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
    path[1] = RIGHT_HASH

    r = self.computeMerkle(tx, proofLen, hash, path)
    expMerkle = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
    return(r == expMerkle)

def testWithin6Confirms():
    self.init333k()
    b0 = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    b1 = 0x000000000000000010e318d0c61da0b84246481d9cc097fda9327fe90b1538c1 # block #333001
    b2 = 0x000000000000000005895c1348171a774e11ee57374680b54a982e9d9e7309a1
    b3 = 0x00000000000000001348f0e7b14d82d8105992f0968faeb533a03c55c3d72365
    b4 = 0x000000000000000004001d114c6c278eb0ad37a3ce3a111cf534dd358896c5b3
    b5 = 0x000000000000000004860a07b991a6cd7cae1327c36c21903b8bbe8d2c316ac5
    b6 = 0x0000000000000000016f889a84b7a06e2d4d90cec924400cf62a6ca3ae67dd46

    self.heaviestBlock = b6

    self.block[b6]._blockHeader._prevBlock = b5
    self.block[b5]._blockHeader._prevBlock = b4
    self.block[b4]._blockHeader._prevBlock = b3
    self.block[b3]._blockHeader._prevBlock = b2
    self.block[b2]._blockHeader._prevBlock = b1
    self.block[b1]._blockHeader._prevBlock = b0

    expB6 = self.within6Confirms(b6) == 1
    expB5 = self.within6Confirms(b5) == 1
    expB1 = self.within6Confirms(b1) == 1
    expB0 = self.within6Confirms(b0) == 0

    return(expB6 and expB5 and expB1 and expB0)

def testConcatHash():
    tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    r = self.concatHash(tx1, tx2)
    return(r == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815)


def testStoreBlockHeader():
    self.init333k()
    version = 2
    hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
    time = 1417792088
    bits = 0x181b7b74
    nonce = 796195988
    blockNumber = 333001

    return(blockNumber == self.storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce))


def testHashHeader():
    version = 2
    hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
    time = 1417792088
    bits = 0x181b7b74
    nonce = 796195988

    expBlockHash = 0x000000000000000010e318d0c61da0b84246481d9cc097fda9327fe90b1538c1
    blockHash = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(blockHash == expBlockHash)


def test__rawHashBlockHeader():
    # https://en.bitcoin.it/wiki/Block_hashing_algorithm
    version = 0x01000000
    hashPrevBlock = 0x81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000
    hashMerkleRoot = 0xe320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b
    time = 0xc7f5d74d
    bits = 0xf2b9441a
    nonce = 0x42a14695

    # these should be the intermediate b1,b2,b3 values inside __rawHashBlockHeader()
    # b1 = 0x0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    # b2 = 0x00000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    # b3 = 0xf1fc122bc7f5d74df2b9441a42a1469500000000000000000000000000000000
    # hash1 = sha256([b1,b2,b3], chars=80)
    # hash2 = sha256([hash1], 1)
    # return(hash2)

    res = self.__rawHashBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    # log(res)

    expHash = 0x1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000
    return res == expHash



def testIsNonceValid():
    ver = 2
    prev_block = 0x000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717
    mrkl_root = 0x871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a
    time_ = 0x53058b35 # 2014-02-20 04:57:25
    bits = 0x19015f53
    nonce = 856192328

    res = self.isNonceValid(ver, prev_block, mrkl_root, time_, bits, nonce)
    return(res)

# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
def testTargetFromBits():
    bits = 0x19015f53
    exp = 8614444778121073626993210829679478604092861119379437256704
    res = self.targetFromBits(bits)
    return(res == exp)

inset('btcrelay.py')
