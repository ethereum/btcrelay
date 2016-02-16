# https://en.bitcoin.it/wiki/Difficulty

with open("../headers/blockchain_headers") as f:
    f.seek(72)
    rev_diff_bits = f.read(4)
    diff_bits = rev_diff_bits[::-1].encode('hex')
    print diff_bits
    # f.seek(80 * startBlock)
    # bhBytes = f.read(80 * count)
