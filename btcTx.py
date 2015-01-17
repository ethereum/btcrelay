
data codeString256
# workaround for now
self.codeString256 = text("0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz")


data pos
data buf

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



def readUInt32LE():
    bb = self.buf
    val = self.flipBytes(bb, 4)
    self.pos += 4
    return(val)


def test_readUInt32LE():
    rawTx = text("03042342")
    size = len(rawTx)
    self.buf = self.str2a(rawTx, outsz=size)
    self.pos = 0
    res = self.readUInt32LE()
    exp = 0x42230403
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
