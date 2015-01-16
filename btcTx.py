
data codeString256
# workaround for now
self.codeString256 = text("0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz")


data pos

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
def strRev2a(string:s, size):
    arr = array(size)
    halfLen = size / 2
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
    halfLen = len(s) / 2
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

def test_read_as_int():
    # tx = '01000000010c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a90000000000ffffffff0100f2052a010000001976a9143744841e13b90b4aca16fe793a7f88da3a23cc7188ac00000000'
    expected = 808464688
    res = self.read_as_int(13)
    return(res)
