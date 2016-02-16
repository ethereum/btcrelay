import sys

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

with open("../headers/blockchain_headers") as f:
    end_block = 2
    chainwork = 0

    for i in range(end_block):
        f.seek(72)
        rev_diff_bits = f.read(4)
        diff_bits = rev_diff_bits[::-1]

        diff_num = targetFromBits(int(diff_bits.encode('hex'), 16))

        denom = diff_num * 0xffff

        chainwork += NUMERATOR / denom

        f.seek(80)

    print str(end_block) + ': ' + str(chainwork)
