
data pos
data buf[]

data tmpScriptLen
data tmpScriptArr[]  # 'id' is 2


# copy 'arr' to global array with given 'id'
def copyToArr(myarr:arr, size, id):
    i = 0
    while i < size:
        if id == 2:
            self.tmpScriptArr[i] = myarr[i]
        i += 1

# returns array
def initFromArr(size, id):
    myarr = array(size)
    i = 0
    # log(size)
    # log(self.pos)
    while i < size:
        if id == 2:
            myarr[i] = self.tmpScriptArr[i]
        # log(myarr[i])
        i += 1
    return(myarr:arr)

# copy 'arr' to global self.buf[]
def copyToBuf(myarr:arr, size):
    i = 0
    while i < size:
        self.buf[i] = myarr[i]
        i += 1

# return an array with the contents of self.buf[] starting for index self.pos
def initFromBuf(size):
    myarr = array(size)
    i = 0
    # log(size)
    # log(self.pos)
    while i < size:
        myarr[i] = self.buf[(self.pos*2) + i]
        # log(myarr[i])
        i += 1
    return(myarr:arr)

def test_initFromBuf():
    size = 3
    self.buf[0] = 1
    self.buf[1] = 3
    self.buf[2] = 5
    bb = self.initFromBuf(size, outsz=size)
    return(bb:arr)


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
    return(bb:arr)


# does not convert to numeric
# make sure caller uses outsz=len*2
def readReverse(len):
    size = len * 2
    bb = self.initFromBuf(size, outsz=size)
    val = self.pair_rev(bb, size, outsz=size)
    self.pos += len # note: len NOT size
    return(val:arr)


def test_readReverse():
    rawTx = text("0c432f4fb3e871a8bda638350b3d5c698cf431db8d6031b53e3fb5159e59d4a9")
    size = len(rawTx)
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)

    self.pos = 0
    res = self.readReverse(32, outsz=64)
    # exp is a9d4599e15b53f3eb531608ddb31f48c695c3d0b3538a6bda871e8b34f2f430c
    # (ord('a') is 97, ord('9') is 57 and this is what will be returned...)
    return(res:arr)  # expect [97, 57, 100, 52, 53 etc] if numeric, expect [10, 9, 13, 4, 5, 9, 9, etc]

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



def parseBlockHeader(rawHeader:str):
    version = self.readUInt32LE()
    prevHash = self.readReverse(32, outsz=64)
    merkleRoot = self.readReverse(32, outsz=64)
    time = self.readUInt32LE()
    bits = self.readUInt32LE()
    nonce = self.readUInt32LE()

    # log(version)
    # prevHashStr = self.a2str(prevHash, 64, outsz=64)
    # log(datastr=prevHashStr)
    # log(time)
    # log(bits)
    # log(nonce)


def test_parseBlockHeader():
    # from https://en.bitcoin.it/wiki/Block_hashing_algorithm, this is blockheader 125552
    rawBlockHeader = text("0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122bc7f5d74df2b9441a42a14695")
    size = len(rawBlockHeader)

    self.__setupForParsingTx(rawBlockHeader, size)
    # meta = self.__getMetaForOutput(outNum, outsz=2)


    #outNum = 0
    # exp hash is untested
    # expHashOfOutputScript = 56502271141207574289324577080259466406131090189524790551966501267826601078627
    res = self.parseBlockHeader(rawBlockHeader)
    #return(res)


def callBtcRelayToStoreHeader(version, hashPrevBlock:arr, hashMerkleRoot:arr, time, bits, nonce):
    # log(version)
    # prevHashStr = self.a2str(hashPrevBlock, 64, outsz=64)
    # log(datastr=prevHashStr)

    nPrev = self.a2int(hashPrevBlock)
    # log(nPrev)

    nMerkle = self.a2int(hashMerkleRoot)
    # log(nMerkle)

    # log(time)
    # log(bits)
    # log(nonce)

    res = self.storeBlockHeader(version, nPrev, nMerkle, time, bits, nonce)
    return(res)


def parseAndStoreHeader(rawHeader:str):
    version = self.readUInt32LE()
    prevHash = self.readReverse(32, outsz=64)
    merkleRoot = self.readReverse(32, outsz=64)
    time = self.readUInt32LE()
    bits = self.readUInt32LE()
    nonce = self.readUInt32LE()

    # log(version)
    # prevHashStr = self.a2str(prevHash, 64, outsz=64)
    # log(datastr=prevHashStr)

    res = self.callBtcRelayToStoreHeader(version, prevHash, merkleRoot, time, bits, nonce)
    return(res)


def test_parseAndStoreHeader():
    # from https://en.bitcoin.it/wiki/Block_hashing_algorithm, this is blockheader 125552
    rawBlockHeader = text("0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122bc7f5d74df2b9441a42a14695")
    size = len(rawBlockHeader)

    self.__setupForParsingTx(rawBlockHeader, size)
    res = self.parseAndStoreHeader(rawBlockHeader)
    return(res)

# def jtestlog(mystring:str):
#     log(datastr=mystring)

def storeRawBlockHeader(rawBlockHeader:str):
    size = len(rawBlockHeader)

    self.__setupForParsingTx(rawBlockHeader, size)
    res = self.parseAndStoreHeader(rawBlockHeader)
    return(res)

def testStoreGenesisBlock():
    # genesis
    rawBlockHeader = text("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
    res = self.storeRawBlockHeader(rawBlockHeader)
    return(res)


def testStoreBlock1():
    # block 1
    rawBlockHeader = text("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299")
    res = self.storeRawBlockHeader(rawBlockHeader)
    return(res)


def testStoringHeaders():
    self.testStoreGenesisBlock()
    res = self.testStoreBlock1()
    return(res)


# heaviestBlock is in btcrelay.py
def logBlockchainHead():
    log(self.heaviestBlock)


# unoptimized
# to get the scriptArr, do this:
# res = self.__getMetaForOutput(0, outsz=2)
# dblSize = res[1]*2   # #res[1] is the scriptSize
# scriptArr = self.__getOutScriptFromTmpArr(dblSize, 2, outsz=dblSize)
# the (standard) output script should be of form 76a914 <hashAddr> 88ac
def __getOutScriptFromTmpArr():
    scriptArr = self.initFromArr(self.tmpScriptLen, 2, outsz=self.tmpScriptLen)  # 2 is the id for tmpScriptArr
    return(scriptArr:arr)



# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr, and outputScriptSize to self.tmpScriptLen
#
# this is needed until can figure out how a dynamically sized array can be returned from a function
# instead of needing 2 functions, one that returns array size, then calling to get the actual array
def getMetaForTxOut(rawTx:str, size, outNum):
    self.__setupForParsingTx(rawTx, size)
    meta = self.__getMetaForOutput(outNum, outsz=2)
    return(meta)



# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr, and outputScriptSize to self.tmpScriptLen
def __getMetaForOutput(outNum):
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

    return(satAndSize:arr)


def __setupForParsingTx(rawTx:str, size):
    bb = self.str2a(rawTx, size, outsz=size)
    self.copyToBuf(bb, size)
    self.pos = 0


def getScriptForTxOut(rawTx:str, size, outNum):
    meta = self.getMetaForTxOut(rawTx, size, outNum, outsz=2)
    scriptArr = self.__getOutScriptFromTmpArr(outsz=self.tmpScriptLen)
    return(scriptArr:arr)


# assumes that scriptArr size is less than 2000
def __checkOutputScript(rawTx:str, size, outNum, expHashOfOutputScript):
    scriptArr = self.getScriptForTxOut(rawTx, size, outNum, outsz=2000)  # hardcoded outsz limit

    scriptStr = self.a2str(scriptArr, self.tmpScriptLen, outsz=self.tmpScriptLen)
    # log(datastr=scriptStr)
    hash = sha256(scriptStr:str)
    # log(hash)
    return(hash == expHashOfOutputScript)

# crashes for some reason TBD
def test_getOutputScript():
    res1 = self.test_getOutput0Script()
    res2 = self.test_getOutput1Script()
    res3 = self.test_getOutputScriptWithMultipleInputs()
    return(res1 == 1 && res2 == 1 && res3 == 1)

def test_getOutputScriptWithMultipleInputs():
    # 3 ins, 2 outs
    rawTx = text("0100000003d64e15b7c11f7532059fe6aacc819b5d886e3aaa602078db57cbae2a8f17cde8000000006b483045022027a176130ebf8bf49fdac27cdc83266a68b19c292b08df1be29f3d964c7e90b602210084ae66b4ff5ed342d78102ef8a4bde87b3ded06929ccaf9a8f71b137baa1816a012102270d473b083897519e5f01c47de7ac50877b6a295775f35966922b3571614370ffffffff54f0e7ded00c01082257eda035d65513b509ddbbe05fae19df0065c294822c9d010000006c493046022100f7423fdbcff22d3cd49921d0af92420d548b925bb1671dc826f15ccc5e05c3de022100d60a6178d892bcf012a79cf9e3430ab70a33b3fa2d156ecf541584e44fa83b150121036674d9607e0461b158c4b3d6368d1869e893cd122c68ebe47af253ff686f064effffffffa6155f8b449da0d3f9d2e1bc8e864c8b78615c1fa560076acaee8802d256a6dd010000006c493046022100e220318b55597c80eecccf9b84f37ab287c14277ccccd269d32f863d8d58d403022100f87818cbed15276f0d5be51aed5bd3b8dea934d6dd2244f2c3170369b96f365501210204b08466f452bb42cefc081ca1c773e26ce0a43566bd9d17b30065c1847072f4ffffffff02301bb50e000000001976a914bdb644fddd802bf7388df220279a18abdf65ebb788ac009ccf6f000000001976a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac00000000")
    outNum = 0
    # exp hash is untested
    expHashOfOutputScript = 56502271141207574289324577080259466406131090189524790551966501267826601078627
    res = self.__checkOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
    return(res)

def test_getOutput0Script():
    rawTx = text("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
    outNum = 0
    # exp hash is untested
    expHashOfOutputScript = 15265305399265587892204941549768278966163359751228226364149342078721216369579
    res = self.__checkOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
    return(res)

def test_getOutput1Script():
    rawTx = text("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
    outNum = 1
    # exp hash is untested
    expHashOfOutputScript = 115071730706014548547567659794968118611083380235397871058495281758347510448362
    res = self.__checkOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
    return(res)


# this may not be needed so holding off on it
# returns an array
# [ version, numIns, ins[ [prevTx, outputIndex, scriptSize, script, seqNumber] ],
# numOuts, outs[ [satoshis, scriptSize, script] ], locktime ]
# def deserialize():


# array to int, eg [48,49, 97, 98] -> 0x01ab
# only handles lowercase a-f
def a2int(in_arr:arr):
    size = len(in_arr)
    result = 0
    i = 0
    while i < size:
        char = in_arr[size-1-i]
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


def test_a2int():
    myarr = array(4)
    myarr[0] = 48
    myarr[1] = 49
    myarr[2] = 97
    myarr[3] = 98
    res = self.a2int(myarr)
    return(res)



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
def str_findChar(mystring:str, char):
    slen = len(mystring)
    i = 0
    while i < slen:
        if getch(mystring, i) == char:
            return(i)
        i += 1
    return(-1)


# reverses in_arr in pairs, for the purpose of reversing bytes
def pair_rev(in_arr:arr, size):
    if size % 2 != 0:
        return(7777777) # error

    if size == 2:
        return([in_arr[0], in_arr[1]], 2)

    myarr = array(size)
    halfLen = size / 2
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = in_arr[i]
        myarr[i] = in_arr[tailIndex-1]
        myarr[tailIndex-1] = tmp
        tmp = in_arr[i+1]
        myarr[i+1] = in_arr[tailIndex]
        myarr[tailIndex] = tmp
        i += 2
    return(myarr:arr)


def test_pair_rev_single():
    size = 2
    myarr = array(2)
    myarr[0] = 1
    myarr[1] = 2
    b = self.pair_rev(myarr, size, outsz=size)
    return(b:arr)  # expect [1, 2]

def test_pair_rev():
    size = 4
    myarr = array(4)
    myarr[0] = 1
    myarr[1] = 2
    myarr[2] = 3
    myarr[3] = 4
    b = self.pair_rev(myarr, size, outsz=size)
    return(b:arr)  # expect [3, 4, 1, 2]



# string reverse to array (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def arr_rev(in_arr:arr, size):
    myarr = array(size)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = in_arr[i]
        myarr[i] = in_arr[tailIndex]
        myarr[tailIndex] = tmp
        i += 1
    return(myarr:arr)

def test_arr_rev():
    myarr = array(3)
    myarr[0] = 1
    myarr[1] = 2
    myarr[2] = 3
    b = self.arr_rev(myarr, 3, outsz=3)
    return(b:arr)

# string to array
def str2a(mystring:str, size):
    myarr = array(size)
    i = 0
    while i < size:
        myarr[i] = getch(mystring, i)
        i += 1
    return(myarr:arr)

def test_str2a():
    mystring = text("abcdef")
    size = len(mystring)
    b = self.str2a(mystring, size, outsz=size)
    return(b:arr)

# string reverse to array (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def strRev2a(mystring:str, size):
    myarr = array(size)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = getch(mystring, i)
        myarr[i] = getch(mystring, tailIndex)
        myarr[tailIndex] = tmp
        i += 1
    return(myarr:arr)

def test_strRev2a():
    mystring = text("abcdef")
    size = len(mystring)
    b = self.strRev2a(mystring, size, outsz=size)
    return(b:arr)

# not working yet (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def str_rev(mystring:str):
    size = len(s)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        oldHead = getch(mystring, i)
        tailIndex = slen - 1 - i
        new = getch(mystring, tailIndex)
        setch(mystring, i, new)
        setch(mystring, tailIndex, oldHead)
        i += 1
    return(mystring:str)

def test_str_rev():
    res = self.str_rev("abc")
    return(res)

def a2str(myarr:arr, size):
    mystr = string(size)

    i = 0
    while i < size:
        setch(mystr, i, myarr[i])
        i += 1

    return(mystr:str)

def test_a2str():
    # mystr = text("cow")
    # log(datastr=mystr)

    myarr = array(3)
    myarr[0] = 99
    myarr[1] = 111
    myarr[2] = 119

    mystr = self.a2str(myarr, 3, outsz=3)
    log(datastr=mystr)


# def test_str_findChar():
#     res = self.str_findChar(self.codeString256, "A")
#     return(res)


# needs to be at bottom, for now https://github.com/ethereum/serpent/issues/44
inset('btcrelay.py')
