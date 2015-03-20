from pyethereum import tester

from bitcoin import *


import datetime
import struct
import pytest
slow = pytest.mark.slow

class TestBtcEth(object):

    CONTRACT = 'btc-eth.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    # tx is fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    TX_STR = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000'
    TX_HASH = int(dbl_sha256(TX_STR.decode('hex')), 16)


    def setup_class(cls):
        tester.gas_limit = 2 * 10**6
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed

    def testTransfer(self):
        assert self.c.setTrustedBtcRelay(self.s.block.coinbase) == 1
        assert self.c.testingonlySetBtcAddr(0xc398efa9c392ba6013c5e04ee729755ef7f58b32) == 1

        res = self.c.processTransfer(self.TX_STR, self.TX_HASH, profiling=True)
        print('GAS: '+str(res['gas']))
        assert(res['output'] == 1)

        expEtherAddr = '948c765a6914d43f2a7ac177da2c2f6b52de3d7c'
        userEthBalance = self.s.block.get_balance(expEtherAddr)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 13
        assert userEthBalance == expEtherBalance

    def testUntrustedCaller(self):
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH, sender=tester.k1)
        assert res == 0

    def testRelayCanClaimWithDifferentTx(self):
        assert self.c.setTrustedBtcRelay(tester.a1) == 1
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH, sender=tester.k1)
        assert res == 1

        anotherHash = self.TX_HASH + 1
        res = self.c.processTransfer(self.TX_STR, anotherHash, sender=tester.k1)
        assert res == 1

    def testRelayCanNotReclaim(self):
        assert self.c.setTrustedBtcRelay(tester.a1) == 1
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH, sender=tester.k1)
        assert res == 1

        # trustedBtcRelay should NOT be able to reclaim
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH, sender=tester.k1)
        assert res == 0

        # owner (k0) can reclaim again
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH, sender=tester.k0)
        assert res == 1

        # change owner and should no longer be able to processTransfer
        nextOwner = 'deadc901078781c232a2a521c2af7980f8385ee9'
        assert self.c.setOwner(nextOwner) == 1
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH)
        assert res == 0


    def testOwnerCanReclaim(self):
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH)
        assert res == 1  # since msg.sender is owner

        # test that owner can reclaim
        res = self.c.processTransfer(self.TX_STR, self.TX_HASH)
        assert res == 1  # since msg.sender is owner

    def testOnlyOwnerPrivs(self):
        nextOwner = 'deadc901078781c232a2a521c2af7980f8385ee9'
        assert self.c.setOwner(nextOwner) == 1

        assert self.c.setTrustedBtcRelay(self.s.block.coinbase) == 0

        # only the new owner can call setOwner
        assert self.c.setOwner(self.s.block.coinbase) == 0
