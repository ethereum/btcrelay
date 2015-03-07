import math

#
# helper functions for relayTx testing
#


# for now, read the bits of n in order (from least significant)
# and convert 0 -> 2 and 1 -> 1
def indexToPath(n, nSibling):
    ret = []
    if n == 0:
        ret = [2] * nSibling
    else:
        bits = int(math.log(n, 2)+1)
        for i in range(bits):
            if checkBit(n, i) == 0:
                ret.append(2)
            else:
                ret.append(1)

        if bits < nSibling:
            ret = ret + ([2] * (nSibling - bits))
    return ret


def checkBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)
