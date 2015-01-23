
data pos
data buf[]

data tmpScriptLen
data tmpScriptArr[]  # 'id' is 2


# copy 'arr' to global array with given 'id'
def copyToArr(arr:a, size, id):
    i = 0
    while i < size:
        if id == 2:
            self.tmpScriptArr[i] = arr[i]
        i += 1

# returns array
def initFromArr(size, id):
    arr = array(size)
    i = 0
    # log(size)
    # log(self.pos)
    while i < size:
        if id == 2:
            arr[i] = self.tmpScriptArr[i]
        # log(arr[i])
        i += 1
    return(arr:a)

# copy 'arr' to global self.buf[]
def copyToBuf(arr:a, size):
    i = 0
    while i < size:
        self.buf[i] = arr[i]
        i += 1

# return an array with the contents of self.buf[] starting for index self.pos
def initFromBuf(size):
    arr = array(size)
    i = 0
    # log(size)
    # log(self.pos)
    while i < size:
        arr[i] = self.buf[(self.pos*2) + i]
        # log(arr[i])
        i += 1
    return(arr:a)

def test_initFromBuf():
    size = 3
    self.buf[0] = 1
    self.buf[1] = 3
    self.buf[2] = 5
    bb = self.initFromBuf(size, outsz=size)
    return(bb:a)


def txinFromBuf():
    prevTxId = self.readReverse(32, outsz=64)
    outputIndex = self.readUInt32LE()
    # log(outputIndex)

    scriptSize = self.readVarintNum()
    # log(scriptSize)

    if scriptSize > 0:
        dblSize = scriptSize*2
        scriptArr = self.readSimple(scriptSize, outsz=dblSize)

    seqNum = self.readUInt32LE()
    # log(seqNum)


# returns satoshis and sets self.tmpScriptLen and self.tmpScriptArr
def txoutFromBuf():
    satoshis = self.readUInt64LE()
    log(satoshis)

    scriptSize = self.readVarintNum()
    log(scriptSize)
    self.tmpScriptLen = scriptSize * 2

    if scriptSize > 0:
        dblSize = scriptSize*2
        scriptArr = self.readSimple(scriptSize, outsz=dblSize)
        self.copyToArr(scriptArr, dblSize, 2)

        # self.tmpScriptArr = scriptArr
        #log(data=scriptArr)


    # mcopy( , scriptArr, scriptSize)

    return([satoshis, scriptSize], 2)


# does not convert to numeric
# make sure caller uses outsz=len*2
def readSimple(len):
    size = len * 2
    bb = self.initFromBuf(size, outsz=size)
    self.pos += len # note: len NOT size
    # log(data=bb)
    return(bb:a)


# does not convert to numeric
# make sure caller uses outsz=len*2
def readReverse(len):
    size = len * 2
    bb = self.initFromBuf(size, outsz=size)
    val = self.pair_rev(bb, size, outsz=size)
    self.pos += len # note: len NOT size
    return(val:a)


def test_readReverse():
    rawTx = text("0c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a9")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readReverse(32, outsz=64)
    # exp is a9d4599e15b53f3eb531608ddb31f48c695c3d0b3538a6bda871e8b34f2f430c
    # (ord('a') is 97, ord('9') is 57 and this is what will be returned...)
    return(res:a)  # expect [97, 57, 100, 52, 53 etc] if numeric, expect [10, 9, 13, 4, 5, 9, 9, etc]

# tested via twip()
def readVarintNum():
    first = self.readUInt8()
    if first == 0xfd:
        return(self.readUInt16LE())
    elif first == 0xfe:
        return(self.readUInt32LE())
    elif first == 0xff:
        return(self.readUInt64LE())
    else:
        return(first)


# unoptimized
# to get the scriptArr, do this:
# res = self.getMetaForOutputNumber(0, outsz=2)
# dblSize = res[1]*2   # #res[1] is the scriptSize
# scriptArr = self.getOutputScript(dblSize, 2, outsz=dblSize)
# the (standard) output script should be of form 76a914 <hashAddr> 88ac
def getOutputScript():
    scriptArr = self.initFromArr(self.tmpScriptLen, 2, outsz=self.tmpScriptLen)  # 2 is the id for tmpScriptArr
    return(scriptArr:a)


# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr, and outputScriptSize to self.tmpScriptLen
def getMetaForOutputNumber(outNum):
    version = self.readUInt32LE()
    # log(version)
    # log(self.pos)
    numIns = self.readVarintNum()
    # log(numIns)
    # log(self.pos)

    i = 0
    while i < numIns:
        self.txinFromBuf()
        i += 1

    numOuts = self.readVarintNum()

    i = 0
    while i <= outNum:
        satAndSize = self.txoutFromBuf(outsz=2)
        i += 1

    return(satAndSize:a)



def test_getOutputScriptWithMultipleInputs():
    # 3 ins, 2 outs
    rawTx = text("0100000003d64e15b7c11f7532059fe6aacc819b5d886e3aaa602078db57cbae2a8f17cde8000000006b483045022027a176130ebf8bf49fdac27cdc83266a68b19c292b08df1be29f3d964c7e90b602210084ae66b4ff5ed342d78102ef8a4bde87b3ded06929ccaf9a8f71b137baa1816a012102270d473b083897519e5f01c47de7ac50877b6a295775f35966922b3571614370ffffffff54f0e7ded00c01082257eda035d65513b509ddbbe05fae19df0065c294822c9d010000006c493046022100f7423fdbcff22d3cd49921d0af92420d548b925bb1671dc826f15ccc5e05c3de022100d60a6178d892bcf012a79cf9e3430ab70a33b3fa2d156ecf541584e44fa83b150121036674d9607e0461b158c4b3d6368d1869e893cd122c68ebe47af253ff686f064effffffffa6155f8b449da0d3f9d2e1bc8e864c8b78615c1fa560076acaee8802d256a6dd010000006c493046022100e220318b55597c80eecccf9b84f37ab287c14277ccccd269d32f863d8d58d403022100f87818cbed15276f0d5be51aed5bd3b8dea934d6dd2244f2c3170369b96f365501210204b08466f452bb42cefc081ca1c773e26ce0a43566bd9d17b30065c1847072f4ffffffff02301bb50e000000001976a914bdb644fddd802bf7388df220279a18abdf65ebb788ac009ccf6f000000001976a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac00000000")
    size = len(rawTx)
    expHashOfOutputScript = 18263457219859066632795018565730871302430616201752059402413209513794416243122
    res = self.t22(rawTx, size, expHashOfOutputScript)
    return(res)

def t22(rawTx:s, size, expHashOfOutputScript):
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)
    self.pos = 0


    meta = self.getMetaForOutputNumber(0, outsz=2)
    scriptArr = self.getOutputScript(outsz=self.tmpScriptLen)

    hash = sha256(scriptArr, self.tmpScriptLen)
    # log(hash)
    return(hash == expHashOfOutputScript)


# test tx has only 1 input
def test_getMetaForOutputNumber():
    res1 = self.test_getOutput0Script()
    res2 = self.test_getOutput1Script()
    return(res1 == 1 && res2 == 1)

# test tx has only 1 input
def setupForTestgetMetaForOutputNumber():
    # only 1 output rawTx = text("01000000010c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a90000000000ffffffff0100f2052a010000001976a9143744841e13b90b4aca16fe793a7f88da3a23cc7188ac00000000")
    rawTx = text("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)
    self.pos = 0


def test_getOutput0Script():
    self.setupForTestgetMetaForOutputNumber()
    res = self.getMetaForOutputNumber(0, outsz=2)
    #res[1] is the scriptSize
    # log(res[1])
    dblSize = res[1]*2
    scriptArr = self.initFromArr(dblSize, 2, outsz=dblSize)
    # return(scriptArr:a)

    hash = sha256(scriptArr, dblSize)
    # log(hash)
    exp = 59193746930381602221929576708645239567127131472230248524131494292030451013368 # not sure how to get this
    return(hash == exp)


def test_getOutput1Script():
    self.setupForTestgetMetaForOutputNumber()
    res = self.getMetaForOutputNumber(1, outsz=2)
    #res[1] is the scriptSize
    # log(res[1])
    dblSize = res[1]*2
    scriptArr = self.initFromArr(dblSize, 2, outsz=dblSize)
    # return(scriptArr:a)

    hash = sha256(scriptArr, dblSize)
    # log(hash)
    exp = 71890310846922344280121795744358198578782792037309011779978844978237080739429 # not sure how to get this
    return(hash == exp)





# this may not be needed so holding off on it
# returns an array
# [ version, numIns, ins[ [prevTx, outputIndex, scriptSize, script, seqNumber] ],
# numOuts, outs[ [satoshis, scriptSize, script] ], locktime ]
# def deserialize():


# only handles lowercase a-f
# tested via tests for readUInt8, readUInt32LE, ...
def readUnsignedBitsLE(bits):
    size = bits / 4
    bb = self.initFromBuf(size, outsz=size)
    # log(bb)

    val = self.pair_rev(bb, size, outsz=size)
    self.pos += size / 2
    # log(self.pos)

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



# char is just a string of length 1
def str_findChar(string:s, char):
    slen = len(string)
    i = 0
    while i < slen:
        if getch(string, i) == char:
            return(i)
        i += 1
    return(-1)


# reverses in_arr in pairs, for the purpose of reversing bytes
def pair_rev(in_arr:a, size):
    if size % 2 != 0:
        return(7777777) # error

    if size == 2:
        return([in_arr[0], in_arr[1]], 2)

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


def test_pair_rev_single():
    size = 2
    arr = array(2)
    arr[0] = 1
    arr[1] = 2
    b = self.pair_rev(arr, size, outsz=size)
    return(b:a)  # expect [1, 2]

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



# def test_str_findChar():
#     res = self.str_findChar(self.codeString256, "A")
#     return(res)
