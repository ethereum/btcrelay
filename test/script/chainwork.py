import sys
import os

DIFFICULTY_1 = 0x00000000FFFF0000000000000000000000000000000000000000000000000000

NUMERATOR = DIFFICULTY_1 * 2**48

# https://en.bitcoin.it/wiki/Difficulty
# chainwork = D * 2**48 / 0xffff
# where D = DIFFICULTY_1 / targetFromBits
# thus chainwork = NUMERATOR / (targetFromBits * 0xffff)


# based on http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
def targetFromBits(bits):
    exp = bits / 0x1000000  # 2**24
    mant = bits & 0xffffff
    return mant * 256**(exp - 3)

# print hex(targetFromBits(0x1b0404cb))
# sys.exit(0)

bits = 486594666
# bits = 486604799
# print DIFFICULTY_1 / targetFromBits(bits) * 2**48 / 0xffff

# print 2**256 / (targetFromBits(bits)+1)

# print (~targetFromBits(bits) / (targetFromBits(bits)+1)) + 1


# print float(DIFFICULTY_1) / targetFromBits(bits)
# print targetFromBits(bits)
# sys.exit(0)

with open("../headers/blockchain_headers") as f:
    end_block = 36288
    chainwork = 0

    f.seek(72, os.SEEK_CUR)
    for i in range(end_block + 1):
        rev_diff_bits = f.read(4)
        diff_bits = rev_diff_bits[::-1]

        diff_num = targetFromBits(int(diff_bits.encode('hex'), 16))

        # denom = diff_num * 0xffff

        block_proof = 2**256 / (diff_num+1)

        chainwork += block_proof

        # chainwork += NUMERATOR / denom

        # chainwork += DIFFICULTY_1 / diff_num * 2**48 / 0xffff

        if i % 2016 == 0:
            print str(i) + ': ' + str(chainwork)
            print ' T=' +  diff_bits.encode('hex') #str(diff_num)
            print (i+1) * 4295032833 == chainwork

        f.seek(76, os.SEEK_CUR)

    print str(end_block) + ': ' + str(chainwork)
