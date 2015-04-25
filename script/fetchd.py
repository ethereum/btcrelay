from datetime import datetime, date
from time import sleep
from argparse import ArgumentParser

from pyepm import api, config
from bitcoin import *

try:
    from urllib.request import build_opener
except:
    from urllib2 import build_opener


BITCOIN_MAINNET = 'btc'
BITCOIN_TESTNET = 'testnet'
SLEEP_TIME = 60 * 10 # 10 mins

# Makes a request to a given URL (first arg) and optional params (second arg)
def make_request(*args):
    opener = build_opener()
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0'+str(random.randrange(1000000)))]
    try:
        return opener.open(*args).read().strip()
    except Exception as e:
        try:
            p = e.read().strip()
        except:
            p = e
        raise Exception(p)



api_config = config.read_config()
instance = api.Api(api_config)


# instance.address = "0xcd2a3d9f938e13cd947ec05abc7fe734df8dd826"
# instance.relayContract = "0xba164d1e85526bd5e27fd15ad14b0eae91c45a93"


def main():
    parser = ArgumentParser()
    parser.add_argument('--fetch', action='store_true', help='fetch blockheaders')
    parser.add_argument('-s', '--sender', required=True, help='sender of transaction')
    parser.add_argument('-r', '--relay', required=True, help='relay contract address')
    parser.add_argument('-n', '--network', default=BITCOIN_TESTNET, choices=[BITCOIN_TESTNET, BITCOIN_MAINNET], help='Bitcoin network')
    parser.add_argument('-d', '--daemon', default=False, action='store_true', help='run as daemon')

    args = parser.parse_args()

    instance.address = args.sender
    instance.relayContract = args.relay

    if not args.daemon:
        run(doFetch=args.fetch)
        return

    while True:
        run(doFetch=args.fetch)
        sleep(SLEEP_TIME)


def run(doFetch=False, network=BITCOIN_TESTNET):
    chainHead = blockHashHex(getBlockchainHead())

    if network == BITCOIN_MAINNET:
        blockInfoUrl = "https://btc.blockr.io/api/v1/block/info/"
    else:
        blockInfoUrl = "https://tbtc.blockr.io/api/v1/block/info/"

    # retry network every 2mins
    for i in range(4):
        while True:
            try:
                data = make_request(blockInfoUrl + chainHead)
            except Exception as e:
                sleep(120)

                if i == 3:
                    return
                continue
            break

    jsonobj = json.loads(data)
    contractHeight = jsonobj["data"]["nb"]

    actualHeight = last_block_height(network)

    print('@@@ heights: {0} {1}').format(contractHeight, actualHeight)

    print('@@@ chainHead: %s' % chainHead)

    chunkSize = 5
    fetchNum =  actualHeight - contractHeight
    numChunk = fetchNum / chunkSize
    leftoverToFetch = fetchNum % chunkSize

    print('@@@ numChunk: {0} leftoverToFetch: {1}').format(numChunk, leftoverToFetch)

    if doFetch:
        fetchHeaders(contractHeight+1, chunkSize, numChunk, network=network)
        fetchHeaders(actualHeight-leftoverToFetch+1, 1, leftoverToFetch, network=network)

        sleep(3)
        print('@@@ chainHead: %s' % chainHead)


def fetchHeaders(chunkStartNum, chunkSize, numChunk, network=BITCOIN_TESTNET):
    for j in range(numChunk):
        strings = ""
        for i in range(chunkSize):
            blockNum = chunkStartNum  + i
            bhJson = blockr_get_block_header_data(blockNum, network=network)
            bhStr = serialize_header(bhJson)
            print("@@@ {0}: {1}").format(blockNum, bhStr)
            strings += bhStr

        storeHeaders(strings.decode('hex'), chunkSize)

        chainHead = getBlockchainHead()
        print('@@@ DONE hexHead: %s' % blockHashHex(chainHead))

        chunkStartNum += chunkSize


def storeHeaders(bhBinary, chunkSize):

    txCount = instance.transaction_count(defaultBlock='pending')
    print('----------------------------------')
    print('txCount: %s' % txCount)

    hashOne = blockHashHex(int(bin_dbl_sha256(bhBinary[:80])[::-1].encode('hex'), 16))
    hashLast = blockHashHex(int(bin_dbl_sha256(bhBinary[-80:])[::-1].encode('hex'), 16))
    print('hashOne: %s' % hashOne)
    print('hashLast: %s' % hashLast)

    firstH = bhBinary[:80].encode('hex')
    lastH = bhBinary[-80:].encode('hex')
    print('firstH: %s' % firstH)
    print('lastH: %s' % lastH)


    fun_name = "bulkStoreHeader"
    sig = "si"

    # bhBinary = '\x02\x00\x00\x00~\xf0U\xe1gM.eQ\xdb\xa4\x1c\xd2\x14\xde\xbb\xee4\xae\xb5D\xc7\xecg\x00\x00\x00\x00\x00\x00\x00\x00\xd3\x99\x89c\xf8\x0c[\xabC\xfe\x8c&"\x8e\x98\xd00\xed\xf4\xdc\xbeH\xa6f\xf5\xc3\x9e-z\x88\\\x91\x02\xc8mSl\x89\x00\x19Y:G\r\x02\x00\x00\x00Tr\xac\x8b\x11\x87\xbf\xcf\x91\xd6\xd2\x18\xbb\xda\x1e\xb2@]|U\xf1\xf8\xcc\x82\x00\x00\x00\x00\x00\x00\x00\x00\xab\n\xaa7|\xa3\xf4\x9b\x15E\xe2\xaek\x06g\xa0\x8fB\xe7-\x8c$\xae#q@\xe2\x8f\x14\xf3\xbb|k\xccmSl\x89\x00\x19\xed\xd8<\xcf\x02\x00\x00\x00\xa9\xab\x12\xe3,\xed\xdc+\xa5\xe6\xade\x1f\xacw,\x986\xdf\x83M\x91\xa0I\x00\x00\x00\x00\x00\x00\x00\x00\xdfuu\xc7\x8f\x83\x1f \xaf\x14~\xa7T\xe5\x84\xaa\xd9Yeiic-\xa9x\xd2\xddq\x86#\xfd0\xc5\xccmSl\x89\x00\x19\xe6Q\x07\xe9\x02\x00\x00\x00,P\x1f\xc0\xb0\xfd\xe9\xb3\xc1\x0e#S\xc1TI*5k\x1a\x02)^+\x86\x00\x00\x00\x00\x00\x00\x00\x00\xa7\xaaa\xc8\xd3|\x88v\xba\xa0\x17\x9ej2\x94D4\xbf\xd3\xe1\xccug\x89*1K\x0c{\x9e]\x92\'\xcemSl\x89\x00\x19\xa4\xa0<{\x02\x00\x00\x00\xe7\xfc\x91>+y\n0v\x0c\xaa\xfb\x9b_\xaa\xe1\xb5\x1dlT\xff\xe4\xae\x82\x00\x00\x00\x00\x00\x00\x00\x00P\xad\x11k\xfb\x11c\x03\x03a\xd9}H\xb4\xca\x90\'\xa4\x9b\xca\xf8\xb8\xd4!\x1b\xaa\x92\xccr\xe7\xe1#f\xcfmSl\x89\x00\x19\xe6\x13\x9c\x82'
    data = [bhBinary, chunkSize]

    gas = 3000000
    gas_price = 10000000000000  # if CPP, may need to make this 10szabo (10e12)
    value = 0


    #
    # store the headers
    #
    wait = True
    from_count = instance.transaction_count(defaultBlock='pending')
    if wait:
        from_block = instance.last_block()

    instance.transact(instance.relayContract, fun_name=fun_name, sig=sig, data=data, gas=gas, gas_price=gas_price, value=value)

    # instance.wait_for_transaction(
    #     from_count=from_count,
    #     #verbose=(True if api_config.get('misc', 'verbosity') > 1 else False))
    #     verbose=True)

    if wait:
        for i in range(1):
            instance.wait_for_next_block(from_block=from_block,
                #verbose=(True if api_config.get('misc', 'verbosity') > 1 else False))
                verbose=True)
            from_block = instance.last_block()

    chainHead = getBlockchainHead()
    expHead = int(bin_dbl_sha256(bhBinary[-80:])[::-1].encode('hex'), 16)

    if chainHead != expHead:
        print('@@@@@ MISMATCH chainHead: {0} expHead: {1}').format(
            blockHashHex(chainHead), blockHashHex(expHead))
        # sys.exit(1)


def getBlockchainHead():
    gas = 3000000
    gas_price = 1

    fun_name = 'getBlockchainHead'
    sig = ''
    data = []

    callResult = instance.call(instance.relayContract, fun_name=fun_name, sig=sig, data=data, gas=gas, gas_price=gas_price)
    chainHead = callResult[0] if len(callResult) else callResult
    return chainHead


def blockHashHex(number):
    hexHead = hex(number)[2:-1] # snip off the 0x and trailing L
    hexHead = '0'*(64-len(hexHead)) + hexHead
    return hexHead

if __name__ == '__main__':
    main()
