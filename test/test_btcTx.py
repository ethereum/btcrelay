from pyethereum import tester

import datetime
import struct
import pytest
slow = pytest.mark.slow

class TestBtcTx(object):

    CONTRACT = 'btcTx.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed


    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def getBlockHeaderBinary(self, ver, prev_block, mrkl_root, time_, bits, nonce):
        bytesPrevBlock = format(prev_block, '64x').replace(' ', '0')
        bytesPrevBlock = bytesPrevBlock.decode('hex')[::-1]

        bytesMerkle = format(mrkl_root, '64x').replace(' ', '0')
        bytesMerkle = bytesMerkle.decode('hex')[::-1]

        header = ( struct.pack("<L", ver) + bytesPrevBlock +
              bytesMerkle + struct.pack("<LLL", time_, bits, nonce))
        return header

    # also tests a (fake) fork
    def testHeadersFrom100K(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeRawBlockHeader(headers[i], blockHeaderBinary[i])
            assert res == i+2


        # block hashes
        b0 = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        b1 = 0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090 # block #100001
        b2 = 0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
        b3 = 0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1
        b4 = 0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79
        b5 = 0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45
        b6 = 0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60

        # values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        proofLen = 2
        hash = [None] * proofLen
        path = [None] * proofLen

        RIGHT_HASH = 2
        hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        path[0] = RIGHT_HASH

        hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
        path[1] = RIGHT_HASH


        txBlockHash = 0xdead
        res = self.c.verifyTx(tx, proofLen, hash, path, txBlockHash)
        assert res == 0

        # b1 is within6confirms so should NOT verify
        txBlockHash = b1
        res = self.c.verifyTx(tx, proofLen, hash, path, txBlockHash)
        assert res == 0


        # verifyTx should only return 1 for b0
        txBlockHash = b0
        res = self.c.verifyTx(tx, proofLen, hash, path, txBlockHash)
        assert res == 1


        # insert (fake) blocks that will not be on main chain
        # using script/mine.py these are the next 7 blocks
        # nonce: 0 blockhash: 11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        # nonce: 0 blockhash: 02c67135bd91986f9aaf3f0818baab439202fe5c34400c2c10bff6cd1336d436
        # nonce: 1 blockhash: 6e60065cc981914c23897143c75f0cde6e456df65f23afd41ddc6e6ce86b2b63
        # nonce: 1 blockhash: 38a052cdf4ef0fddf2de88e687163db7f39cb8de738fa9f5e871a72fc74c57c1
        # nonce: 0 blockhash: 2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c
        EASIEST_DIFFICULTY_TARGET = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = EASIEST_DIFFICULTY_TARGET
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBinary = self.getBlockHeaderBinary(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce, blockHeaderBinary)
            hashPrevBlock = self.c.fastHashBlock(blockHeaderBinary)
            assert res == i+2

        # forked block should NOT verify
        txBlockHash = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, proofLen, hash, path, txBlockHash)
        assert res == 0

        # b0 should still verify
        txBlockHash = b0
        res = self.c.verifyTx(tx, proofLen, hash, path, txBlockHash)
        assert res == 1


    # test that a tx that verifies, does not verify after a reorg causes it to
    # no longer be on the main chain
    def testReorg(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)



        # tx for verification: values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        proofLen = 2
        hash = [None] * proofLen
        path = [None] * proofLen

        RIGHT_HASH = 2
        hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        path[0] = RIGHT_HASH

        hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
        path[1] = RIGHT_HASH



        # insert (easy) blocks
        # using script/mine.py these are the next 7 blocks
        # nonce: 0 blockhash: 11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        # nonce: 0 blockhash: 178930a916fa91dd29b2716387b7e024a6b3b2d2efa86bc45c86be223b07a4e5
        # nonce: 0 blockhash: 7b3c348edbb3645b34b30259105a941890e95e0ecc0a1c243ff48260d746e456
        # nonce: 0 blockhash: 02c67135bd91986f9aaf3f0818baab439202fe5c34400c2c10bff6cd1336d436
        # nonce: 1 blockhash: 6e60065cc981914c23897143c75f0cde6e456df65f23afd41ddc6e6ce86b2b63
        # nonce: 1 blockhash: 38a052cdf4ef0fddf2de88e687163db7f39cb8de738fa9f5e871a72fc74c57c1
        # nonce: 0 blockhash: 2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c
        EASIEST_DIFFICULTY_TARGET = 0x207fFFFFL
        version = 1
        # real merkle of block100k
        hashMerkleRoot = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        time = 1293623863  # from block100k
        bits = EASIEST_DIFFICULTY_TARGET
        nonce = 1
        hashPrevBlock = block100kPrev
        for i in range(7):
            nonce = 1 if (i in [4,5]) else 0
            blockHeaderBinary = self.getBlockHeaderBinary(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
            res = self.c.storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce, blockHeaderBinary)
            hashPrevBlock = self.c.fastHashBlock(blockHeaderBinary)
            assert res == i+2

        # testingonlySetHeaviest is needed because the difficulty from
        # EASIEST_DIFFICULTY_TARGET becomes 0 and so the score does not
        # increase, meaning that heaviesBlock also does not change
        self.c.testingonlySetHeaviest(0x2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c)

        firstEasyBlock = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, proofLen, hash, path, firstEasyBlock)
        assert res == 1


        # reorg: add headers with more PoW (difficulty)
        # add headers one by one and tx should only be verified when the
        # last header is added, ie tx has enough confirmations
        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        block100k = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        for i in range(7):
            res = self.c.storeRawBlockHeader(headers[i], blockHeaderBinary[i])
            assert res == i+2

            # firstEasyBlock should no longer verify since it is no longer on the main chain
            res = self.c.verifyTx(tx, proofLen, hash, path, firstEasyBlock)
            assert res == 0

            # block100k should only verify when it has enough confirmations
            res = self.c.verifyTx(tx, proofLen, hash, path, block100k)
            exp = 1 if i==6 else 0
            assert res == exp



    def testWithin6Confirms(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeRawBlockHeader(headers[i], blockHeaderBinary[i])
            assert res == i+2


        blockHash = [
            0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506,
            0x00000000000080b66c911bd5ba14a74260057311eaeb1982802f7010f1a9f090, # block #100001
            0x0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af,
            0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1,
            0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79,
            0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45,
            0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60
        ]

        for i, bh in enumerate(blockHash):
            res = self.c.within6Confirms(bh)
            exp = 0 if i==0 else 1
            assert res == exp


    def storeGenesisBlock(self):
        blockHeaderStr = ("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeRawBlockHeader(blockHeaderStr, bhBinary)
        assert res == 1

    def storeBlock1(self):
        # block 1
        blockHeaderStr = ("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299")
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeRawBlockHeader(blockHeaderStr, bhBinary)
        assert res == 2


    def testStoringHeaders(self):
        self.storeGenesisBlock()
        self.storeBlock1()


    def testHashBlock(self):
        rawBlockHeader = "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710"
        res = self.c.hashBlock(rawBlockHeader)
        exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        assert res == exp


    def testFastHashBlock(self):
        blockHeaderStr = "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710"
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.fastHashBlock(bhBinary)
        exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        assert res == exp


    # @pytest.mark.skipif(True,reason='crash like crash604branch')
    def test_getOutputScriptWithMultipleInputs(self):
        # 3 ins, 2 outs
        rawTx = ("0100000003d64e15b7c11f7532059fe6aacc819b5d886e3aaa602078db57cbae2a8f17cde8000000006b483045022027a176130ebf8bf49fdac27cdc83266a68b19c292b08df1be29f3d964c7e90b602210084ae66b4ff5ed342d78102ef8a4bde87b3ded06929ccaf9a8f71b137baa1816a012102270d473b083897519e5f01c47de7ac50877b6a295775f35966922b3571614370ffffffff54f0e7ded00c01082257eda035d65513b509ddbbe05fae19df0065c294822c9d010000006c493046022100f7423fdbcff22d3cd49921d0af92420d548b925bb1671dc826f15ccc5e05c3de022100d60a6178d892bcf012a79cf9e3430ab70a33b3fa2d156ecf541584e44fa83b150121036674d9607e0461b158c4b3d6368d1869e893cd122c68ebe47af253ff686f064effffffffa6155f8b449da0d3f9d2e1bc8e864c8b78615c1fa560076acaee8802d256a6dd010000006c493046022100e220318b55597c80eecccf9b84f37ab287c14277ccccd269d32f863d8d58d403022100f87818cbed15276f0d5be51aed5bd3b8dea934d6dd2244f2c3170369b96f365501210204b08466f452bb42cefc081ca1c773e26ce0a43566bd9d17b30065c1847072f4ffffffff02301bb50e000000001976a914bdb644fddd802bf7388df220279a18abdf65ebb788ac009ccf6f000000001976a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac00000000")
        outNum = 0
        # exp hash is untested
        expHashOfOutputScript = 56502271141207574289324577080259466406131090189524790551966501267826601078627
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1


    def test_getOutput0Script(self):
        # 1 ins, 1 outs
        rawTx = ("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
        outNum = 0
        # exp hash is untested
        expHashOfOutputScript = 15265305399265587892204941549768278966163359751228226364149342078721216369579
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1

    def test_getOutput1Script(self):
        # 1 ins, 1 outs
        rawTx = ("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
        outNum = 1
        # exp hash is untested
        expHashOfOutputScript = 115071730706014548547567659794968118611083380235397871058495281758347510448362
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1



    # this was for debugging a bug that was caused by a missing initAncestorDepths()
    @pytest.mark.skipif(True,reason='skip')
    def testtq(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        # self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        for i in range(7):
            res = self.c.storeRawBlockHeader(headers[i])
            assert res == i+2

        self.c.logAnc(0x000000000002a0a74129007b1481d498d0ff29725e9f403837d517683abac5e1)
        self.c.logAnc(0x000000000000b0b8b4e8105d62300d63c8ec1a1df0af1c2cdbd943b156a8cd79)
        self.c.logAnc(0x000000000000dab0130bbcc991d3d7ae6b81aa6f50a798888dfe62337458dc45)
        self.c.logAnc(0x0000000000009b958a82c10804bd667722799cc3b457bc061cd4b7779110cd60)
