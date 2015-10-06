
# based on http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
#
import hashlib, struct

# EASIEST_DIFFICULTY_TARGET = 0x1d00ffff
EASIEST_DIFFICULTY_TARGET = 0x207fFFFF

block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250

ver = 1
#prev_block = "000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717"
# mrkl_root = "871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a"
#time_ = 0x53058b35 # 2014-02-20 04:57:25
#bits = 0x19015f53

mrkl_root = "f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766"
time_ = 1293623863  # from block100k
bits = EASIEST_DIFFICULTY_TARGET

prev_block = "000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250"


# https://en.bitcoin.it/wiki/Difficulty
exp = bits >> 24
mant = bits & 0xffffff
target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
target_str = target_hexstr.decode('hex')



for i in range(7):

    nonce = 0
    while nonce < 0x100000000:
        header = ( struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
              mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time_, bits, nonce))
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        # print nonce, hash[::-1].encode('hex')
        if hash[::-1] < target_str:
            print 'success: ' + str(nonce) + ' blockhash: ' + hash[::-1].encode('hex')
            break
        nonce += 1

    prev_block = str(hash[::-1].encode('hex'))
    # print('prev_block: '+prev_block)
    # prev_block = str(hash[::-1])
