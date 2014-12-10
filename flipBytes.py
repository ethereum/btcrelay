data byte[32]

def flipBytes(n):
    mask = 0xff
    i = 0
    while i < 32:
        b = n & mask
        b /= 2^(i*8)
        b *= 2^((31-i)*8)
        mask *= 256
        byte[i] = b

    return(byte)
