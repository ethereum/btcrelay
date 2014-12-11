def flipBytes(n):
    byte = array(32)
    numByte = 32
    mask = 0xff
    i = 0
    while i < numByte:
        b = n & mask
        b /= 2^(i*8)
        b *= 2^((numByte-i-1)*8)
        mask *= 256
        byte[i] = b
        i += 1

    ret = byte[0]
    i = 1
    while i < numByte:
        ret = ret | byte[i]
        i += 1

    return(ret)
