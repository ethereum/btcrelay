data byte[32]

def flipBytes(n):
    numByte = 3
    mask = 0xff
    i = 0
    while i < numByte:
        b = n & mask
        b /= 2^(i*8)
        b *= 2^((numByte-i-1)*8)
        mask *= 256
        byte[i] = b
        i += 1

    ret = byte[0] | byte[1] | byte[2]
    return(ret)
