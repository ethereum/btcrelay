byte = [1,2,3,4,5]

def flipBytes(n):
    numByte = 5
    mask = 0xff
    i = 0
    while i < numByte:
        b = n & mask
        b /= 2 ** (i*8)
        b *= 2 ** ((numByte-i-1)*8)
        mask *= 256
        byte[i] = b
        i += 1

    ret = byte[0]
    i = 1
    while i < numByte:
        ret = ret | byte[i]
        i += 1


    # byte[4] = 0
    # ret = byte[0]
    # ret = ret | byte[1]
    # ret = ret | byte[2]
    # ret = ret | byte[3]
    # ret = ret | byte[4]


    return ret

ans = flipBytes(0xabcdef)
print 'ans: ' + str(ans)
