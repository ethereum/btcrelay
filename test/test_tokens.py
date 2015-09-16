from ethereum import tester
from datetime import datetime, date
# from functools import partial

import time
# import random

import pytest
slow = pytest.mark.slow

from utilRelay import makeMerkleProof, randomMerkleProof, disablePyethLogging

disablePyethLogging()


# from contracts.json via Truffle
TOKEN_FACTORY_BINARY = '60606040526110f6806100136000396000f30060606040526000357c01000000000000000000000000000000000000000000000000000000009004806305215b2f1461004f5780635f8dead31461008c578063dc3f65d3146100cf5761004d565b005b610060600480359060200150610231565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100a3600480359060200180359060200150610124565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6100da600450610175565b60405180806020018281038252838181518152602001915080519060200190602002808383829060006004602084601f0104600302600f01f1509050019250505060405180910390f35b60006000506020528160005260406000206000508181548110156100025790600052602060002090016000915091509054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6020604051908101604052806000815260200150600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005080548060200260200160405190810160405280929190818152602001828054801561022257602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16815260200190600101908083116101ee575b5050505050905061022e565b90565b600060006000600084604051610c8d8061046983390180828152602001915050604051809103906000f092508291508173ffffffffffffffffffffffffffffffffffffffff1663c86a90fe8633604051837c0100000000000000000000000000000000000000000000000000000000028152600401808381526020018273ffffffffffffffffffffffffffffffffffffffff168152602001925050506020604051808303816000876161da5a03f1156100025750505060405151506001600060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000508181540191508181548183558181151161036957818360005260206000209182019101610368919061034a565b80821115610364576000818150600090555060010161034a565b5090565b5b505050905082600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060018303815481101561000257906000526020600020900160006101000a81548173ffffffffffffffffffffffffffffffffffffffff0219169083021790555080600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081815481835581811511610454578183600052602060002091820191016104539190610435565b8082111561044f5760008181506000905550600101610435565b5090565b5b50505050829350610460565b50505091905056006060604052604051602080610c8d8339016040526060805190602001505b80600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b50610c2b806100626000396000f300606060405236156100b6576000357c0100000000000000000000000000000000000000000000000000000000900480631fa03a2b146100b857806321af4feb146100e557806327e235e314610112578063673448dd1461013957806367eae67214610160578063930b7a2314610193578063bbd39ac0146101ac578063c86a90fe146101d3578063d26c8a8a14610200578063daea85c514610221578063f4b1604514610234578063fbf1f78a14610261576100b6565b005b6100cf600480359060200180359060200150610ace565b6040518082815260200191505060405180910390f35b6100fc600480359060200180359060200150610c00565b6040518082815260200191505060405180910390f35b610123600480359060200150610bb0565b6040518082815260200191505060405180910390f35b61014a6004803590602001506109ed565b6040518082815260200191505060405180910390f35b61017d6004803590602001803590602001803590602001506103a8565b6040518082815260200191505060405180910390f35b6101aa600480359060200180359060200150610789565b005b6101bd600480359060200150610674565b6040518082815260200191505060405180910390f35b6101ea600480359060200180359060200150610274565b6040518082815260200191505060405180910390f35b61020b600450610638565b6040518082815260200191505060405180910390f35b6102326004803590602001506106b2565b005b61024b600480359060200180359060200150610bcb565b6040518082815260200191505060405180910390f35b610272600480359060200150610851565b005b600082600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156103985782600060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555082600060005060008473ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146856040518082815260200191505060405180910390a3600190506103a2566103a1565b600090506103a2565b5b92915050565b6000600083600060005060008773ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015156106265760009050600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161561045c57600190508050610525565b600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505484111515610524576001905080506000600260005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055505b5b60018114156106185783600060005060008773ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555083600060005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168573ffffffffffffffffffffffffffffffffffffffff167f16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146866040518082815260200191505060405180910390a36001915061063056610621565b60009150610630565b61062f565b60009150610630565b5b509392505050565b6000600060005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050549050610671565b90565b6000600060005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506106ad565b919050565b6001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060016040518082815260200191505060405180910390a35b50565b80600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e836040518082815260200191505060405180910390a35b5050565b6000600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908302179055506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f0e40f4b0b06b7d270eb92aed48caf256e6bbe4f83c5492e7433958cf5566192060006040518082815260200191505060405180910390a38073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fcc92c05edef6bc5dcdfab43862409620fd81888eec1be99935f19375c4ef704e60006040518082815260200191505060405180910390a35b50565b60006001600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610aba57506000600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610ac85760019050610ac9565b5b919050565b60006001600160005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161480610b9b57506000600260005060008573ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054115b15610ba95760019050610baa565b5b92915050565b60006000506020528060005260406000206000915090505481565b60016000506020528160005260406000206000506020528060005260406000206000915091509054906101000a900460ff1681565b600260005060205281600052604060002060005060205280600052604060002060009150915050548156'
TOKEN_FACTORY_ABI = '[{"inputs":[{"type":"uint256","name":"_initialAmount"}],"constant":false,"name":"createStandardToken","outputs":[{"type":"address","name":""}],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"uint256","name":""}],"constant":true,"name":"created","outputs":[{"type":"address","name":""}],"type":"function"},{"inputs":[],"constant":false,"name":"createdByMe","outputs":[{"type":"address[]","name":""}],"type":"function"}]';

TOKEN_CONTRACT_ABI = '[{"inputs":[{"type":"address","name":"_target"},{"type":"address","name":"_proxy"}],"constant":true,"name":"isApprovedFor","outputs":[{"type":"bool","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"address","name":""}],"constant":true,"name":"approved_once","outputs":[{"type":"uint256","name":""}],"type":"function"},{"inputs":[{"type":"address","name":""}],"constant":true,"name":"balances","outputs":[{"type":"uint256","name":""}],"type":"function"},{"inputs":[{"type":"address","name":"_proxy"}],"constant":true,"name":"isApproved","outputs":[{"type":"bool","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_from"},{"type":"uint256","name":"_value"},{"type":"address","name":"_to"}],"constant":false,"name":"sendCoinFrom","outputs":[{"type":"bool","name":"_success"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":true,"name":"who","outputs":[{"type":"address","name":"_r"}],"type":"function"},{"inputs":[],"constant":true,"name":"sendr","outputs":[{"type":"address","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"},{"type":"uint256","name":"_maxValue"}],"constant":false,"name":"approveOnce","outputs":[],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":true,"name":"coinBalanceOf","outputs":[{"type":"uint256","name":"_r"}],"type":"function"},{"inputs":[{"type":"uint256","name":"_value"},{"type":"address","name":"_to"}],"constant":false,"name":"sendCoin","outputs":[{"type":"bool","name":"_success"}],"type":"function"},{"inputs":[],"constant":true,"name":"coinBalance","outputs":[{"type":"uint256","name":"_r"}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":false,"name":"approve","outputs":[],"type":"function"},{"inputs":[{"type":"address","name":""},{"type":"address","name":""}],"constant":true,"name":"approved","outputs":[{"type":"bool","name":""}],"type":"function"},{"inputs":[{"type":"address","name":"_addr"}],"constant":false,"name":"unapprove","outputs":[],"type":"function"},{"inputs":[{"type":"uint256","name":"_initialAmount"}],"type":"constructor"},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"uint256","name":"value"}],"type":"event","name":"CoinTransfer","anonymous":false},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"bool","name":"result"}],"type":"event","name":"AddressApproval","anonymous":false},{"inputs":[{"indexed":true,"type":"address","name":"from"},{"indexed":true,"type":"address","name":"to"},{"indexed":false,"type":"uint256","name":"value"}],"type":"event","name":"AddressApprovalOnce","anonymous":false}]'

TOKEN_ENDOWMENT = 2**200
REWARD_PER_HEADER = 1000
FEE_VERIFY_TX = 12 * REWARD_PER_HEADER


def initBtcRelayTokens(cls, tester):
    tfAddr = cls.s.evm(TOKEN_FACTORY_BINARY.decode('hex'))
    _abi = TOKEN_FACTORY_ABI
    TOKEN_FACTORY = tester.ABIContract(cls.s, _abi, tfAddr, listen=True, log_listener=None)

    tokenContractAddr = cls.c.initTokenContract(TOKEN_FACTORY.address)

    _abi = TOKEN_CONTRACT_ABI
    _address = hex(tokenContractAddr)[2:-1].decode('hex')
    cls.xcoin = tester.ABIContract(cls.s, _abi, _address, listen=True, log_listener=None)


class TestTokens(object):

    CONTRACT = 'btcrelay.se'
    # BTC_ETH_CONTRACT = 'test/btc-eth_debug.se'

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = int(2.55e6)  # include costs of debug methods
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)

        initBtcRelayTokens(cls, tester)

        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    # based on test_txVerify test30BlockValidTx
    def testChargeOneVerifyTx(self):
        numHeader = 30
        keySender = tester.k0
        addrSender = tester.a0
        self.storeHeadersFrom300K(numHeader, keySender, addrSender)

        # block 300017
        header = {'nonce': 2022856018, 'hash': u'000000000000000032c0ae55f7f52b179a6346bb0d981af55394a3b9cdc556ea', 'timestamp': 1399708353, 'merkle_root': u'2fcb4296ba8d2cc5748a9310bac31d2652389c4d70014ccf742d0e4409a612c9', 'version': 2, 'prevhash': u'00000000000000002ec86a542e2cefe62dcec8ac2317a1dc92fbb094f9d30941', 'bits': 419465580}
        hashes = [u'29d2afa00c4947965717542a9fcf31aa0d0f81cbe590c9b794b8c55d7a4803de', u'84d4e48925445ef3b5722edaad229447f6ef7c77dfdb3b67b288a2e9dac97ebf', u'9f1ddd2fed16b0615d8cdd99456f5229ff004ea93234256571972d8c4eda05dd', u'ca31ee6fecd2d054b85449fb52d2b2bd9f8777b5e603a02d7de53c09e300d127', u'521eabbe29ce215b4b309db7807ed8f655ddb34233b2cfe8178522a335154923', u'a03159699523335896ec6d1ce0a18b247a3373b288cefe6ed5d14ddeeb71db45', u'810a3a390a4b565a54606dd0921985047cf940070b0c61a82225fc742aa4a2e3', u'161400e37071b7096ca6746e9aa388e256d2fe8816cec49cdd73de82f9dae15d', u'af355fbfcf63b67a219de308227dca5c2905c47331a8233613e7f7ac4bacc875', u'1c433a2359318372a859c94ace4cd2b1d5f565ae2c8496ef8255e098c710b9d4', u'49e09d2f48a8f11e13864f7daca8c6b1189507511a743149e16e16bca1858f80', u'5fd034ffd19cda72a78f7bacfd7d9b7b0bc64bc2d3135382db29238aa4d3dd03', u'74ab68a617c8419e6cbae05019a2c81fea6439e233550e5257d9411677845f34', u'df2650bdfcb4efe5726269148828ac18e2a1990c15f7d01d572252656421e896', u'1501aa1dbcada110009fe09e9cec5820fce07e4178af45869358651db4e2b282', u'41f96bb7e58018722c4d0dae2f6f4381bb1d461d3a61eac8b77ffe274b535292', u'aaf9b4e66d5dadb4b4f1107750a18e705ce4b4683e161eb3b1eaa04734218356', u'56639831c523b68cac6848f51d2b39e062ab5ff0b6f2a7dea33765f8e049b0b2', u'3a86f1f34e5d4f8cded3f8b22d6fe4b5741247be7ed164ca140bdb18c9ea7f45', u'da0322e4b634ec8dac5f9b173a2fe7f6e18e5220a27834625a0cfe6d0680c6e8', u'f5d94d46d68a6e953356499eb5d962e2a65193cce160af40200ab1c43228752e', u'e725d4efd42d1213824c698ef4172cdbab683fe9c9170cc6ca552f52244806f6', u'e7711581f7f9028f8f8b915fa0ddb091baade88036bf6f309e2d802043c3231d']
        [txHash, txIndex, siblings, txBlockHash] = makeMerkleProof(header, hashes, 1)

        self.xcoin.approveOnce(self.c.address, FEE_VERIFY_TX)
        res = self.c.verifyTx(txHash, txIndex, siblings, txBlockHash, profiling=True)
        print('GAS: '+str(res['gas']))
        assert res['output'] == 1  # adjust according to numHeader and the block that the tx belongs to

        expCoinsOfSender = numHeader*REWARD_PER_HEADER - FEE_VERIFY_TX
        assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender
        assert self.xcoin.coinBalanceOf(self.c.address) == TOKEN_ENDOWMENT - expCoinsOfSender


    def storeHeadersFrom300K(self, numHeader, keySender, addrSender):
        startBlockNum = 300000

        block300kPrev = 0x000000000000000067ecc744b5ae34eebbde14d21ca4db51652e4d67e155f07e
        self.c.setInitialParent(block300kPrev, startBlockNum-1, 1)

        expCoinsOfSender = 0
        i = 1
        with open("test/headers/100from300k.txt") as f:

            startTime = datetime.now().time()

            for header in f:
                res = self.c.storeBlockHeader(header[:-1].decode('hex'), sender=keySender)  # [:-1] to remove \n
                assert res == i-1+startBlockNum

                expCoinsOfSender += REWARD_PER_HEADER
                assert self.xcoin.coinBalanceOf(addrSender) == expCoinsOfSender
                assert self.xcoin.coinBalanceOf(self.c.address) == TOKEN_ENDOWMENT - expCoinsOfSender

                if i==numHeader:
                    break
                i += 1

            endTime = datetime.now().time()

        # duration = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
        # print("********** duration: "+str(duration)+" ********** start:"+str(startTime)+" end:"+str(endTime))


    # based on test_btcrelay testStoreBlockHeader
    def testRewardOneBlock(self):
        bal = self.xcoin.coinBalanceOf(self.c.address)
        assert bal == TOKEN_ENDOWMENT

        block300K = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
        self.c.setInitialParent(block300K, 299999, 1)

        blockHeaderStr = '0200000059c786bb379b65487f373279354f8ccc91ffcea2200c36080000000000000000dd9d7757a736fec629ab0ed0f602ba23c77afe7edec85a7026f641fd90bcf8f658ca8154747b1b1894fc742f'
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.storeBlockHeader(bhBinary, profiling=True, sender=tester.k1)
        print('GAS: %s' % res['gas'])
        assert res['output'] == 300000

        assert self.xcoin.coinBalanceOf(tester.a1) == REWARD_PER_HEADER

        bal = self.xcoin.coinBalanceOf(self.c.address)
        assert bal == TOKEN_ENDOWMENT - REWARD_PER_HEADER


#
#
#
# reward valid store & no reward negative test (fork)
#
#             # no coin rewards for fake blocks
#             assert self.xcoin.coinBalanceOf(tester.a0) == 0
#             assert self.xcoin.coinBalanceOf(self.c.address) == expOwnerBal
