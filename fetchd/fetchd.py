#!/usr/bin/env python

# from datetime import datetime, date
from time import sleep
from argparse import ArgumentParser

import logging

from pyepm import api, config, __version__
from bitcoin import *  # NOQA


BITCOIN_MAINNET = 'btc'
BITCOIN_TESTNET = 'testnet'
SLEEP_TIME = 5 * 60  # 5 mins.  If changing, check retry logic
GAS_FOR_STORE_HEADERS = 1200000  # it should take less than 1M gas, but buffer to avoid running out

CHUNK_SIZE = 5  # number of headers to fetch at a time
CHUNK_RANGE = range(CHUNK_SIZE)

api_config = config.read_config()
instance = api.Api(api_config)

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

pyepmLogger = logging.getLogger("pyepm")
pyepmLogger.setLevel(logging.INFO)

# instance.address = "0xcd2a3d9f938e13cd947ec05abc7fe734df8dd826"
# instance.relayContract = "0xba164d1e85526bd5e27fd15ad14b0eae91c45a93"
# TESTNET relay: 0x142f674e911cc55c226af81ac4d6de0a671d4abf

useWallet = False  # when True, need to set the following remaining values:
instance.walletContract = ''  # address of the contract wallet
instance.weiRefill = int(1e18)  # 1 ETH.  Amount to refill the "hot" wallet each time walletWithdraw() is called
aWalletOwner = ''  # address of an owner of the contract wallet


def main():
    # logging.basicConfig(level=logging.DEBUG)
    logger.info("fetchd using PyEPM %s" % __version__)

    parser = ArgumentParser()
    parser.add_argument('-s', '--sender', required=True, help='sender of transaction')
    parser.add_argument('-r', '--relay', required=True, help='relay contract address')

    parser.add_argument('--rpcHost', default='127.0.0.1', help='RPC hostname')
    parser.add_argument('--rpcPort', default='8545', type=int, help='RPC port')
    parser.add_argument('--startBlock', default=0, type=int, help='block number to start fetching from')
    parser.add_argument('-w', '--waitFor', default=0, type=int, help='number of blocks to wait between fetches')
    parser.add_argument('--gasPrice', default=int(10e12), type=int, help='gas price')  # default 10 szabo
    parser.add_argument('--fetch', action='store_true', help='fetch blockheaders')
    parser.add_argument('-n', '--network', default=BITCOIN_TESTNET, choices=[BITCOIN_TESTNET, BITCOIN_MAINNET], help='Bitcoin network')
    parser.add_argument('-d', '--daemon', default=False, action='store_true', help='run as daemon')
    parser.add_argument('--feeVTX', default=0, type=int, help='fee to charge for verifications')
    parser.add_argument('--feeRecipient', help='address of fee recipient')

    args = parser.parse_args()

    instance.address = args.sender
    instance.relayContract = args.relay

    instance.rpcHost = args.rpcHost
    instance.rpcPort = args.rpcPort
    instance.jsonrpc_url = "http://%s:%s" % (instance.rpcHost, instance.rpcPort)

    instance.numBlocksToWait = args.waitFor  # for CPP eth as of Apr 28, 3 blocks seems reasonable.  0 seems to be fine for Geth
    # instance.gasPrice = args.gasPrice

    feeVerifyTx = args.feeVTX
    logger.info('feeVTX: %s' % feeVerifyTx)

    if useWallet:
        if instance.walletContract == '' or aWalletOwner == '':
            logger.info('wallet contract and owner address need to both be set')
            sys.exit()
        if instance.address != aWalletOwner:
            logger.info('sender is not a wallet owner: %s' % instance.address)
            sys.exit()

    feeRecipient = args.feeRecipient or instance.address
    logger.info('feeRecipient: %s' % feeRecipient)

    if feeRecipient != instance.address and not useWallet:
        logger.warn('feeRecipient %s is not sender %s and contract wallet is not used' % (feeRecipient, instance.address))
        sys.exit()

    # logger.info('@@@ rpc: %s' % instance.jsonrpc_url)

    # this can't be commented out easily since run() always does instance.heightToStartFetch = getLastBlockHeight() + 1 for retries
    # contractHeight = getLastBlockHeight()  # needs instance.relayContract to be set
    # logger.info('@@@ contract height: {0} gp: {1}').format(contractHeight, instance.gasPrice)
    # instance.heightToStartFetch = args.startBlock or contractHeight + 1

    # this will not handle exceptions or do retries.  need to use -d switch if desired
    if not args.daemon:
        run(feeVerifyTx, feeRecipient, doFetch=args.fetch, network=args.network, startBlock=args.startBlock)
        return

    while True:
        for i in range(4):
            try:
                run(feeVerifyTx, feeRecipient, doFetch=args.fetch, network=args.network, startBlock=args.startBlock)
                sleep(SLEEP_TIME)
            except Exception as e:
                logger.info(e)
                logger.info('Retry in 1min')
                sleep(60)
                continue
            except:  # catch *all* exceptions
                e = sys.exc_info()[0]
                logger.info(e)
                logger.info('Rare exception')
                raise
            break


def run(feeVerifyTx, feeRecipient, doFetch=False, network=BITCOIN_TESTNET, startBlock=0):
    chainHead = getBlockchainHead()
    if not chainHead:
        raise ValueError("Empty BlockchainHead returned.")
    chainHead = blockHashHex(chainHead)
    logger.info('BTC BlockchainHead: %s' % chainHead)

    # loop in case contract stored correct HEAD, but reorg in *Ethereum* chain
    # so that contract lost the correct HEAD.  we try 3 times since it would
    # be quite unlucky for 5 Ethereum reorgs to coincide with storing the
    # non-orphaned Bitcoin block
    nTime = 5
    for i in range(nTime):
        # refetch if needed in case contract's HEAD was orphaned
        if startBlock:
            contractHeight = startBlock
        else:
            contractHeight = getLastBlockHeight()
        realHead = blockr_get_block_header_data(contractHeight, network=network)['hash']
        heightToRefetch = contractHeight
        while chainHead != realHead:
            logger.info('@@@ chainHead: {0}  realHead: {1}'.format(chainHead, realHead))
            fetchHeaders(heightToRefetch, 1, 1, feeVerifyTx, feeRecipient, network=network)

            # wait for some blocks because Geth has a delay (at least in RPC), of
            # returning the correct data.  the non-orphaned header may already
            # be in the Ethereum blockchain, so we should give it a chance before
            # adjusting realHead to the previous parent
            #
            # realHead is adjusted to previous parent in the off-chance that
            # there is more than 1 orphan block
            # for j in range(4):
            instance.wait_for_next_block(from_block=instance.last_block(), verbose=True)

            chainHead = blockHashHex(getBlockchainHead())
            realHead = blockr_get_block_header_data(heightToRefetch, network=network)['hash']

            heightToRefetch -= 1

            if heightToRefetch < contractHeight - 10:
                if i == nTime - 1:
                    # this really shouldn't happen since 2 orphans are already
                    # rare, let alone 10
                    logger.info('@@@@ TERMINATING big reorg? {0}'.format(heightToRefetch))
                    sys.exit()
                else:
                    logger.info('@@@@ handle orphan did not succeed iteration {0}'.format(i))
                    break  # start the refetch again, this time ++i
        break  # chainHead is same realHead

    actualHeight = last_block_height(network)  # pybitcointools 1.1.33

    if startBlock:
        instance.heightToStartFetch = startBlock
    else:
        instance.heightToStartFetch = getLastBlockHeight() + 1

    logger.info('@@@ startFetch: {0} actualHeight: {1}'.format(instance.heightToStartFetch, actualHeight))

    chunkSize = CHUNK_SIZE
    fetchNum = actualHeight - instance.heightToStartFetch + 1
    numChunk = fetchNum / chunkSize
    leftoverToFetch = fetchNum % chunkSize

    logger.info('@@@ numChunk: {0} leftoverToFetch: {1}'.format(numChunk, fetchNum))
    logger.info('----------------------------------')

    if doFetch:
        fetchHeaders(instance.heightToStartFetch, chunkSize, numChunk, feeVerifyTx, feeRecipient, network=network)
        fetchHeaders(actualHeight - leftoverToFetch + 1, 1, leftoverToFetch, feeVerifyTx, feeRecipient, network=network)
        # sys.exit()


def fetchHeaders(chunkStartNum, chunkSize, numChunk, feeVerifyTx, feeRecipient, network=BITCOIN_TESTNET):
    for j in range(numChunk):
        strings = ""
        for i in range(chunkSize):
            blockNum = chunkStartNum + i
            bhJson = blockr_get_block_header_data(blockNum, network=network)
            bhStr = serialize_header(bhJson)
            logger.info("@@@ {0}: {1}".format(blockNum, bhStr))
            logger.debug("Block header: %s" % repr(bhStr.decode('hex')))
            strings += bhStr

        storeHeaders(strings.decode('hex'), chunkSize, feeVerifyTx, feeRecipient)

        chainHead = getBlockchainHead()
        logger.info('@@@ DONE hexHead: %s' % blockHashHex(chainHead))
        logger.info('==================================')

        chunkStartNum += chunkSize


        # average of 6*24=144 headers a day.  So AROUND every 100 headers we check
        # the balance of sender and if it's less than 1 ETH, we ask for more ETH
        # from the wallet.
        # CHUNK_RANGE is used when chunkSize>1 so that we ask for ETH if chunkStartNum ends in
        # ????00, ????01, ????02 to ????04
        if ((chunkSize == 1 and chunkStartNum % 100 == 0) or
            (chunkSize == CHUNK_SIZE and chunkStartNum % 100 in CHUNK_RANGE)) and useWallet:
            myWei = instance.balance_at(instance.address)
            myBalance = myWei / 1e18
            logger.info('myBalance ETH: %s' % myBalance)

            if myBalance < 1:
                logger.info('going to walletWithdraw')
                walletWithdraw()
                myWei = instance.balance_at(instance.address)
                myBalance = myWei / 1e18
                logger.info('topped up ETH balance: %s' % myBalance)


def storeHeaders(bhBytes, chunkSize, feeVerifyTx, feeRecipient):

    txCount = instance.transaction_count(defaultBlock='pending')
    logger.info('----------------------------------')
    logger.info('txCount: %s' % txCount)

    hashOne = blockHashHex(int(bin_dbl_sha256(bhBytes[:80])[::-1].encode('hex'), 16))
    hashLast = blockHashHex(int(bin_dbl_sha256(bhBytes[-80:])[::-1].encode('hex'), 16))
    logger.info('hashOne: %s' % hashOne)
    logger.info('hashLast: %s' % hashLast)

    firstH = bhBytes[:80].encode('hex')
    lastH = bhBytes[-80:].encode('hex')
    logger.info('firstH: %s' % firstH)
    logger.info('lastH: %s' % lastH)

    sig = 'bulkStoreHeader:[bytes,int256]:int256'

    data = [bhBytes, chunkSize]

    gas = GAS_FOR_STORE_HEADERS
    value = 0

    #
    # Store the headers
    #

    if feeVerifyTx != 0:
        sig = 'storeBlockWithFeeAndRecipient:[bytes,int256,int256]:int256'

    for i in range(chunkSize):
        if feeVerifyTx != 0:
            offset = 80*i
            data = [ bhBytes[offset:offset+80] , feeVerifyTx, feeRecipient]

        # Wait for the transaction and retry if failed
        txHash = instance.transact(instance.relayContract, sig=sig, data=data, gas=gas, value=value)
        logger.info("store header txHash: %s" % txHash)
        txResult = False
        while txResult is False:
            txResult = instance.wait_for_transaction(transactionHash=txHash, defaultBlock="pending", retry=30, verbose=True)
            logger.info("store header pendingblock txResult: %s" % txResult)
            if txResult is False:
                txHash = instance.transact(instance.relayContract, sig=sig, data=data, gas=gas, value=value)

        # Wait for the transaction to be mined and retry if failed
        txResult = False
        while txResult is False:
            txResult = instance.wait_for_transaction(transactionHash=txHash, defaultBlock="latest", retry=60, verbose=True)
            logger.info("store header latestblock txResult: %s" % txResult)
            if txResult is False:
                txHash = instance.transact(instance.relayContract, sig=sig, data=data, gas=gas, value=value)

        if feeVerifyTx == 0:
            break

    chainHead = getBlockchainHead()
    expHead = int(bin_dbl_sha256(bhBytes[-80:])[::-1].encode('hex'), 16)

    if chainHead != expHead:
        logger.info('@@@@@ MISMATCH chainHead: {0} expHead: {1}'.format(blockHashHex(chainHead), blockHashHex(expHead)))
        # sys.exit(1)


def walletWithdraw():
    # execute(address _to, uint _value, bytes _data)
    sig = 'execute:[address,uint256,bytes]:bytes32'
    data = [instance.address, instance.weiRefill, '']
    gas = 999000

    # Wait for the transaction retry if failed
    txHash = instance.transact(instance.walletContract, sig=sig, data=data, gas=gas)
    logger.info("walletWithdraw txHash: %s" % txHash)
    txResult = False
    while txResult is False:
        txResult = instance.wait_for_transaction(transactionHash=txHash, defaultBlock="pending", retry=30, verbose=True)
        if txResult is False:
            txHash = instance.transact(instance.walletContract, sig=sig, data=data, gas=gas)

    # Wait for the transaction to be mined and retry if failed
    txResult = False
    while txResult is False:
        txResult = instance.wait_for_transaction(transactionHash=txHash, defaultBlock="latest", retry=60, verbose=True)
        if txResult is False:
            txHash = instance.transact(instance.walletContract, sig=sig, data=data, gas=gas)


def getLastBlockHeight():
    sig = 'getLastBlockHeight:[]:int256'
    data = []

    pyepmLogger.setLevel(logging.WARNING)
    callResult = instance.call(instance.relayContract, sig=sig, data=data)
    pyepmLogger.setLevel(logging.INFO)
    logger.debug("RESULT %s" % callResult)
    chainHead = callResult[0] if len(callResult) else callResult
    return chainHead


def getBlockchainHead():
    sig = 'getBlockchainHead:[]:int256'
    data = []

    pyepmLogger.setLevel(logging.WARNING)
    callResult = instance.call(instance.relayContract, sig=sig, data=data)
    pyepmLogger.setLevel(logging.INFO)
    chainHead = callResult[0] if len(callResult) else callResult
    return chainHead


def blockHashHex(number):
    hexHead = hex(number)[2:-1]  # snip off the 0x and trailing L
    hexHead = '0' * (64 - len(hexHead)) + hexHead
    return hexHead

if __name__ == '__main__':
    main()
