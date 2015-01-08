
data codeString256
# workaround for now
self.codeString256 = text("0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz")


data pos

self.pos = 0

def test():
    #res = self.test_str_findChar()
    res = self.test_decode()
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
def str_findChar(string, char):
    slen = len(string)
    i = 0
    while i < slen:
        if getch(string, i) == char:
            return(i)
        i += 1
    return(-1)


def test_str_findChar():
    res = self.str_findChar(self.codeString256, '2')
    return(res)


def test_decode():
    res = self.decode(text("0010"), 256)
    return(res)
    # expected = 808464688
    # return(res == expected)

def test_read_as_int():
    # tx = '01000000010c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a90000000000ffffffff0100f2052a010000001976a9143744841e13b90b4aca16fe793a7f88da3a23cc7188ac00000000'
    expected = 808464688
    res = self.read_as_int(13)
    return(res)
