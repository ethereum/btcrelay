from ethereum import tester

import datetime
import struct
import pytest
slow = pytest.mark.slow

from utilRelay import dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestBtcRelay(object):
    CONTRACT_DEBUG = 'test/btcrelay_debug.se'

    TOKEN_FACTORY_BINARY = '60606040526110e8806100136000396000f30060606040526000357c01000000000000000000000000000000000000000000000000000000009004806305215b2f1461004f5780635f8dead31461008c578063dc3f65d3146100cf5761004d565b005b610060600480359060200150610231565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100a3600480359060200180359060200150610124565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600450610175565b60405180806020018281038252838181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f1509050019250505060405180910390f35b60006000506020528160005260406000206000508181548110156100025790600052602060002090016000915091509054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6020604051908101604052806000815260200150600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005080548060200260200160405190810160405280929190818152602001828054801561022257602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16815260200190600101908083116101ee575b5050505050905061022e565b90565b600060006000600084604051610c7f8061046983390180828152602001915050604051809103906000f092508291508173ffffffffffffffffffffffffffffffffffffffff1663c86a90fe8633604051837c0100000000000000000000000000000000000000000000000000000000028152600401808381526020018273ffffffffffffffffffffffffffffffffffffffff168152602001925050506020604051808303816000876161da5a03f1156100025750505060405151506001600060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000508181540191508181548183558181151161036957818360005260206000209182019101610368919061034a565b80821115610364576000818150600090555060010161034a565b5090565b5b505050905082600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060018303815481101561000257906000526020600020900160006101000a81548173ffffffffffffffffffffffffffffffffffffffff0219169083021790555080600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081815481835581811511610454578183600052602060002091820191016104539190610435565b8082111561044f5760008181506000905550600101610435565b5090565b5b50505050829350610460565b50505091905056006060604052604051602080610c7f8339016040526060805190602001505b80600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b50610c1d806100626000396000f300606060405236156100b6576000357c0100000000000000000000000000000000000000000000000000000000900480631fa03a2b146100b857806321af4feb146100e557806327e235e314610112578063673448dd1461013957806367eae67214610160578063930b7a2314610193578063bbd39ac0146101ac578063c86a90fe146101d3578063d26c8a8a14610200578063daea85c514610221578063f4b1604514610234578063fbf1f78a14610261576100b6565b005b6100cf600480359060200180359060200150610ac0565b6040518082815260200191505060405180910390f35b6100fc600480359060200180359060200150610bf2565b6040518082815260200191505060405180910390f35b610123600480359060200150610ba2565b6040518082815260200191505060405180910390f35b61014a6004803590602001506109df565b6040518082815260200191505060405180910390f35b61017d6004803590602001803590602001803590602001506103a8565b6040518082815260200191505060405180910390f35b6101aa60048035906020018035906020015061077b565b005b6101bd600480359060200150610666565b6040518082815260200191505060405180910390f35b6101ea600480359060200180359060200150610274565b6040518082815260200191505060405180910390f35b61020b60045061062a565b6040518082815260200191505060405180910390f35b6102326004803590602001506106a4565b005b61024b600480359060200180359060200150610bbd565b6040518082815260200191505060405180910390f35b610272600480359060200150610843565b005b600082600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156103985782600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555082600060005060008473ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146856040518082815260200191505060405180910390a3600190506103a2566103a1565b600090506103a2565b5b92915050565b6000600083600060005060008773ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156106215760009050600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161561045c57600190508050610524565b600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054841015610523576001905080506000600260005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b5b60018114156106175783600060005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555083600060005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146866040518082815260200191505060405180910390a36001915061062256610620565b60009150610622565b5b5b509392505050565b6000600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050549050610663565b90565b6000600060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061069f565b919050565b6001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060016040518082815260200191505060405180910390a35b50565b80600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e836040518082815260200191505060405180910390a35b5050565b6000600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060006040518082815260200191505060405180910390a38073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e60006040518082815260200191505060405180910390a35b50565b60006001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610aac57506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610aba5760019050610abb565b5b919050565b60006001600160005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610b8d57506000600260005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610b9b5760019050610b9c565b5b92915050565b60006000506020528060005260406000206000915090505481565b60016000506020528160005260406000206000506020528060005260406000206000915091509054906101000a900460ff1681565b600260005060205281600052604060002060005060205280600052604060002060009150915050548156'
    TOKEN_FACTORY_ABI = '[{"constant":false,"inputs":[{"name":"_initialAmount","type":"uint256"}],"name":"createStandardToken","outputs":[{"name":"","type":"address"}],"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"name":"created","outputs":[{"name":"","type":"address"}],"type":"function"},{"constant":false,"inputs":[],"name":"createdByMe","outputs":[{"name":"","type":"address[]"}],"type":"function"}]'

    # obtained via 0.1.2 solc --abi contract.sol
    TOKEN_CONTRACT_ABI = '[{"constant":true,"inputs":[{"name":"_target","type":"address"},{"name":"_proxy","type":"address"}],"name":"isApprovedFor","outputs":[{"name":"_r","type":"bool"}],"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"approved_once","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[{"name":"_proxy","type":"address"}],"name":"isApproved","outputs":[{"name":"_r","type":"bool"}],"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_value","type":"uint256"},{"name":"_to","type":"address"}],"name":"sendCoinFrom","outputs":[{"name":"_success","type":"bool"}],"type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"},{"name":"_maxValue","type":"uint256"}],"name":"approveOnce","outputs":[],"type":"function"},{"constant":true,"inputs":[{"name":"_addr","type":"address"}],"name":"coinBalanceOf","outputs":[{"name":"_r","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"},{"name":"_to","type":"address"}],"name":"sendCoin","outputs":[{"name":"_success","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"coinBalance","outputs":[{"name":"_r","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"approve","outputs":[],"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"approved","outputs":[{"name":"","type":"bool"}],"type":"function"},{"constant":false,"inputs":[{"name":"_addr","type":"address"}],"name":"unapprove","outputs":[],"type":"function"},{"inputs":[{"name":"_initialAmount","type":"uint256"}],"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"CoinTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"result","type":"bool"}],"name":"AddressApproval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"AddressApprovalOnce","type":"event"}]'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(2.55e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT_DEBUG, endowment=2000*cls.ETHER)
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
        self.c.setInitialParent(block100kPrev, 99999, 1)

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
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            # print('@@@@ real chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000

        cumulDiff = self.c.getCumulativeDifficulty()

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
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49


        txBlockHash = 0xdead
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0

        # b1 is within6confirms so should NOT verify
        txBlockHash = b1
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0


        # verifyTx should only return 1 for b0
        txBlockHash = b0
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 1

        assert b6 == self.c.getBlockchainHead()


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
            res = self.c.storeBlockHeader(blockHeaderBinary)
            hashPrevBlock = dblSha256Flip(blockHeaderBinary)

            # print('@@@@ fake chain score: ' + str(self.c.getCumulativeDifficulty()))
            assert res == i+100000

        assert self.c.getCumulativeDifficulty() == cumulDiff  # cumulDiff should not change
        assert b6 == self.c.getBlockchainHead()

        # forked block should NOT verify
        txBlockHash = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 0

        # b0 should still verify
        txBlockHash = b0
        res = self.c.verifyTx(tx, txIndex, sibling, txBlockHash)
        assert res == 1


    # test that a tx that verifies, does not verify after a reorg causes it to
    # no longer be on the main chain
    def testReorg(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)



        # tx for verification: values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49




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
            res = self.c.storeBlockHeader(blockHeaderBinary)
            hashPrevBlock = dblSha256Flip(blockHeaderBinary)
            assert res == i+100000

        # testingonlySetHeaviest is needed because the difficulty from
        # EASIEST_DIFFICULTY_TARGET becomes 0 and so the score does not
        # increase, meaning that heaviesBlock also does not change
        self.c.testingonlySetHeaviest(0x2b80a2f4b68e9ebfd4975f5f14a340501d24c3adf041ad9be4cd2576e827328c)

        firstEasyBlock = 0x11bb7c5555b8eab7801b1c4384efcab0d869230fcf4a8f043abad255c99105f8
        res = self.c.verifyTx(tx, txIndex, sibling, firstEasyBlock)
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
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+100000

            # firstEasyBlock should no longer verify since it is no longer on the main chain
            res = self.c.verifyTx(tx, txIndex, sibling, firstEasyBlock)
            assert res == 0

            # block100k should only verify when it has enough confirmations
            res = self.c.verifyTx(tx, txIndex, sibling, block100k)
            exp = 1 if i==6 else 0
            assert res == exp



    def testWithin6Confirms(self):
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.setInitialParent(block100kPrev, 99999, 1)

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
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+100000


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
            res = self.c.within6Confirms(bh, profiling=True)
            print('GAS: '+str(res['gas']))
            exp = 0 if i==0 else 1
            assert res['output'] == exp


    def storeGenesisBlock(self):
        self.c.setInitialParent(0, 0, 1)

        blockHeaderStr = ("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBinary, profiling=True)
        return res

    def storeBlock1(self):
        # block 1
        blockHeaderStr = ("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299")
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBinary, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == 2  # genesis block is at height 1


    def testStoringHeaders(self):
        res = self.storeGenesisBlock()
        print('GAS: '+str(res['gas']))
        assert res['output'] == 1

        self.storeBlock1()

        block1Hash = 0x00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048
        assert self.c.getBlockchainHead() == block1Hash
        assert self.c.getLastBlockHeight() == 1 + 1  # +1 since setInitialParent was called with imaginary block

        assert self.c.getCumulativeDifficulty() == 2 + 1  # +1 since setInitialParent was called with imaginary block


    def testStoreNewHead(self):
        parent = 0x00000000000000000a15bda775b0004fca6368c5b8a61cb0d3b793670b9369c2
        height = 357368
        cumulDifficulty = 1981747039106115  # 1981795846593359 - 48807487244 (diff at 357369)
        self.c.setInitialParent(parent, height, cumulDifficulty)

        orphanStr = '03000000c269930b6793b7d3b01ca6b8c56863ca4f00b075a7bd150a0000000000000000391c579bd59cb0199baf96dc1bc1066de0dc202bbe18f062a20aa25f78729376ba6f5d55f586161826f45178'
        bhBinary = orphanStr.decode('hex')

        orphanHash = 0x00000000000000000db6ab0aa23c28fc707f05f1646d25dba684ffe316bcf24d
        assert dblSha256Flip(bhBinary) == orphanHash

        assert self.c.storeBlockHeader(bhBinary) == height + 1
        assert self.c.getBlockchainHead() == orphanHash
        assert self.c.getLastBlockHeight() == height + 1
        assert self.c.getCumulativeDifficulty() == 1981795846593359

        # real 357369
        headerStr = '03000000c269930b6793b7d3b01ca6b8c56863ca4f00b075a7bd150a00000000000000004bdc09e5405944a6319baf5e90335f221d5b91d44f5212c05bb1e751b997cc74db6f5d55f5861618351ec186'
        bhBinary = headerStr.decode('hex')

        hash357369 = 0x000000000000000007f379bc159a38fa5ccec4689336f32eba9d148b5c190439
        assert dblSha256Flip(bhBinary) == hash357369

        assert self.c.storeBlockHeader(bhBinary) == height + 1
        assert self.c.getBlockchainHead() == hash357369
        assert self.c.getLastBlockHeight() == height + 1
        assert self.c.getCumulativeDifficulty() == 1981795846593359


    def testStoreExistingHeader(self):
        res = self.storeGenesisBlock()
        g1 = res['gas']
        print('GAS: %s' % g1)
        assert res['output'] == 1

        res = self.storeGenesisBlock()
        g2 = res['gas']
        print('GAS: %s' % g2)
        assert res['output'] == 0 # no block stored
        assert g2 < 0.36 * g1  # 0.36 is as of aae201c


    def testStoreBlockHeader(self):

        # serpent = __import__('serpent')
        # evm = serpent.compile(self.CONTRACT_DEBUG)
        # print('@@@@ evm: '+evm)

        tfAddr = self.s.evm(self.TOKEN_FACTORY_BINARY.decode('hex'))
        _abi = self.TOKEN_FACTORY_ABI
        TOKEN_FACTORY = tester.ABIContract(self.s, _abi, tfAddr, listen=True, log_listener=None)
        # assert BTC_ETH.setTrustedBtcRelay(self.c.address, sender=tester.k1) == 1

        # self.c.setTokenContract(TOKEN_FACTORY.address)
        tokenContractAddr = self.c.setTokenContract(TOKEN_FACTORY.address)

        block300K = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        self.c.setInitialParent(block300K, 299999, 1)

        # version = 2
        # hashPrevBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        # hashMerkleRoot = 0xf6f8bc90fd41f626705ac8de7efe7ac723ba02f6d00eab29c6fe36a757779ddd
        # time = 1417792088
        # bits = 0x181b7b74
        # nonce = 796195988
        # blockNumber = 333001
        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBinary, profiling=True)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        TOKEN_CONTRACT = tester.ABIContract(self.s, self.TOKEN_CONTRACT_ABI, tokenContractAddr, listen=True, log_listener=None)
        TOKEN_CONTRACT.coinBalance()
        # print(TOKEN_CONTRACT.coinBalance())

    # was converted to macro
    # def testFastHashBlock(self):
    #     blockHeaderStr = "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710"
    #     bhBinary = blockHeaderStr.decode('hex')
    #     res = self.c.fastHashBlock(bhBinary, profiling=True)
    #     print('GAS: '+str(res['gas']))
    #     exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
    #     assert res['output'] == exp

    def testComputeMerkle(self):
        # values are from block 100K
        txHash = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        txIndex = 0
        sibling = [None] * 2
        sibling[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        sibling[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49

        res = self.c.computeMerkle(txHash, txIndex, sibling, profiling=True)
        print('GAS: '+str(res['gas']))
        expMerkle = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        wrappedMerkle = res['output'] % 2**256
        assert wrappedMerkle == expMerkle

    def testsetInitialParentOnlyOnce(self):
        assert self.c.setInitialParent(0, 0, 1) == 1
        assert self.c.setInitialParent(0, 0, 1) == 0


    #
    # macro tests start
    #

    def testTargetFromBits(self):
        bits = 0x19015f53
        exp = 8614444778121073626993210829679478604092861119379437256704
        res = self.c.funcTargetFromBits(bits)
        assert res == exp

    def testConcatHash(self):
        tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        r = self.c.funcConcatHash(tx1, tx2)
        assert r % 2**256 == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815

    #
    # end of macro tests
    #
