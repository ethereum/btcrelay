
data codeString256
# workaround for now
self.codeString256 = text("0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz")


data pos
data buf[]

self.pos = 0



def f1(string:s):
    setch(string, 0, "a")
    setch(string, 1, "b")
    return(string)

def t1():
    string = text("cd")
    res = self.f1(string)
    return([getch(res,0), getch(res,1)]:a)  # should return [97,98]
    return(getch(res,1))   # how to get "ab" ?

def logt():
    # log(1)
    # log(1, 2)
    # log(1, 2, 3)
    # log(1, 2, 3, 4)
    log(data=[1,2,3])
    log(1, data=[1,2,3])
    log(1, 2, data=[1,2,3])
    log(1, 2, 3, data=[1,2,3])
    log(1, 2, 3, 4, data=[1,2,3])


def test():
    res = self.test_str_rev()
    # res = self.test_str_findChar()
    #res = self.test_decode()
    return(res)


def read_as_int(bytez):
    self.pos += bytez
    return(self.pos)



def flipBytes(n, numByte):
    mask = 0xff

    result = 0
    i = 0
    while i < numByte:
        b = n & mask
        b = div(b, 2^(i*8))
        b *= 2^((numByte-i-1)*8)
        mask *= 256
        result = result | b
        i += 1

    return(result)

# shift left
def shiftLeft(n, x):
    return(n * 2^x)

# shift right
def shiftRight(n, x):
    return(div(n, 2^x))


def copyToBuf(arr:a, size):
    i = 0
    while i < size:
        self.buf[i] = arr[i]
        i += 1


def initFromBuf(size):
    arr = array(size)
    i = 0
    while i < size:
        arr[i] = self.buf[i]
        i += 1
    return(arr:a)

def test_initFromBuf():
    size = 3
    self.buf[0] = 1
    self.buf[1] = 3
    self.buf[2] = 5
    bb = self.initFromBuf(size, outsz=size)
    return(bb:a)




def t3():
    s = text("7")
    char = getch(s, 0)
    return(char)  # how to convert to 7 (instead of 55)


# only handles lowercase a-f
# tested via tests for readUInt8, readUInt32LE, ...
def readUnsignedBitsLE(bits):
    size = bits / 4
    bb = self.initFromBuf(size, outsz=size)

    val = self.pair_rev(bb, size, outsz=size)
    self.pos += size / 2

    result = 0
    i = 0
    while i < size:
        char = val[size-1-i]
        # log(char)
        if (char >= 97 && char <= 102):  # only handles lowercase a-f
            numeric = char - 87
        else:
            numeric = char - 48

        # log(numeric)

        result += numeric * 16^i
        # log(result)

        i += 1
    return(result)

def readUInt8():
    return self.readUnsignedBitsLE(8)


def test_readUInt8_simple():
    rawTx = text("02")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt8()
    exp = 2
    return(res == exp)

def test_readUInt8():
    t1 = self.test_readUInt8_simple()
    t2 = self.test_readUInt8_hex()
    return(t1 == 1 && t2 == 1)

def test_readUInt8_hex():
    rawTx = text("3c")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt8()
    exp = 60
    return(res == exp)


def readUInt16LE():
    return self.readUnsignedBitsLE(16)

def test_readUInt16LE_hex():
    rawTx = text("89ab")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt16LE()
    exp = 0xab89
    return(res == exp)


# only handles lowercase a-f
def readUInt32LE():
    return self.readUnsignedBitsLE(32)


def test_readUInt32LE():
    t1 = self.test_readUInt32LE_simple()
    t2 = self.test_readUInt32LE_hex()
    t3 = self.test_readUInt32LE_nodejs()
    return(t1 == 1 && t2 == 1 && t3 == 1)

def test_readUInt32LE_simple():
    rawTx = text("01000000")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt32LE()
    exp = 1
    return(res == exp)


def test_readUInt32LE_hex():
    # rawTx = text("03042342")
    rawTx = text("0f000000")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt32LE()
    exp = 15
    return(res == exp)

# test from http://nodejs.org/api/buffer.html#buffer_buf_readuint32le_offset_noassert
def test_readUInt32LE_nodejs():
    rawTx = text("03042342")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt32LE()
    exp = 0x42230403
    return(res == exp)


def readUInt64LE():
    return self.readUnsignedBitsLE(64)

def test_readUInt64LE_hex():
    rawTx = text("abcdef0123456789")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readUInt64LE()
    exp = 0x8967452301efcdab
    return(res == exp)


# not generic, eg assumes base is 256
def decode(string:s, base):
    slen = len(string)
    result = 0
    i = 0
    while i < slen:
        result *= base
        result += getch(string, i)
        i += 1
    return(result)



# char is just a string of length 1
def str_findChar(string:s, char):
    slen = len(string)
    i = 0
    while i < slen:
        if getch(string, i) == char:
            return(i)
        i += 1
    return(-1)



def pair_rev(in_arr:a, size):
    if size % 2 != 0:
        return(7777777) # error

    arr = array(size)
    halfLen = size / 2
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = in_arr[i]
        arr[i] = in_arr[tailIndex-1]
        arr[tailIndex-1] = tmp
        tmp = in_arr[i+1]
        arr[i+1] = in_arr[tailIndex]
        arr[tailIndex] = tmp
        i += 2
    return(arr:a)


def test_pair_rev():
    size = 4
    arr = array(4)
    arr[0] = 1
    arr[1] = 2
    arr[2] = 3
    arr[3] = 4
    b = self.pair_rev(arr, size, outsz=size)
    return(b:a)  # expect [3, 4, 1, 2]



# string reverse to array (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def arr_rev(in_arr:a, size):
    arr = array(size)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = in_arr[i]
        arr[i] = in_arr[tailIndex]
        arr[tailIndex] = tmp
        i += 1
    return(arr:a)

def test_arr_rev():
    arr = array(3)
    arr[0] = 1
    arr[1] = 2
    arr[2] = 3
    b = self.arr_rev(arr, 3, outsz=3)
    return(b:a)

# string to array
def str2a(string:s, size):
    arr = array(size)
    i = 0
    while i < size:
        arr[i] = getch(string, i)
        i += 1
    return(arr:a)

def test_str2a():
    string = text("abcdef")
    size = len(string)
    b = self.str2a(string, size, outsz=size)
    return(b:a)

# string reverse to array (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def strRev2a(string:s, size):
    arr = array(size)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = getch(string, i)
        arr[i] = getch(string, tailIndex)
        arr[tailIndex] = tmp
        i += 1
    return(arr:a)

def test_strRev2a():
    string = text("abcdef")
    size = len(string)
    b = self.strRev2a(string, size, outsz=size)
    return(b:a)

# not working yet (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def str_rev(string:s):
    size = len(s)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        oldHead = getch(string, i)
        tailIndex = slen - 1 - i
        new = getch(string, tailIndex)
        setch(string, i, new)
        setch(string, tailIndex, oldHead)
        i += 1
    return(string:s)

def test_str_rev():
    res = self.str_rev("abc")
    return(res)



def test_str_findChar():
    res = self.str_findChar(self.codeString256, "A")
    return(res)


def test_decode():
    res = self.decode(text("0010"), 256)
    expected = 808464688
    return(res == expected)

def test_deserialize():
    rawTx = text("01000000010c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a90000000000ffffffff0100f2052a010000001976a9143744841e13b90b4aca16fe793a7f88da3a23cc7188ac00000000")
    # version <- get 4 chars, flip, then decode
    return(13)

def test_read_as_int():
    # tx = '01000000010c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a90000000000ffffffff0100f2052a010000001976a9143744841e13b90b4aca16fe793a7f88da3a23cc7188ac00000000'
    expected = 808464688
    res = self.read_as_int(13)
    return(res)
