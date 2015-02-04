
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



def storeRawBlockHeader(rawBlockHeader:str):
    size = len(rawBlockHeader)

    self.__setupForParsingTx(rawBlockHeader, size)
    res = self.parseAndStoreHeader(rawBlockHeader)
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


# only handles lowercase a-f
# tested via tests for readUInt8, readUInt32LE, ...
def readUnsignedBitsLE(bits):
    size = bits / 4


    bb = self.initFromBuf(size, outsz=size)
    # log(bb)

    # val = self.pair_rev(bb, size, outsz=size)
    # log(self.pos)




    result = 0
    j = 0
    while j < size:
        # "01 23 45" want it to read "10 32 54"
        if j % 2 == 0:
            i = j + 1
        else:
            i = j - 1

        log(i)

        char = bb[i]
        # log(char)
        if (char >= 97 && char <= 102):  # only handles lowercase a-f
            numeric = char - 87
        else:
            numeric = char - 48

        # log(numeric)

        result += numeric * 16^j
        # log(result)

        j += 1


    # important
    self.pos += size / 2

    return(result)

def readUInt8():
    return self.readUnsignedBitsLE(8)


def readUInt16LE():
    return self.readUnsignedBitsLE(16)


# only handles lowercase a-f
def readUInt32LE():
    return self.readUnsignedBitsLE(32)


def readUInt64LE():
    return self.readUnsignedBitsLE(64)


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



# string to array
def str2a(mystring:str, size):
    myarr = array(size)
    i = 0
    while i < size:
        myarr[i] = getch(mystring, i)
        i += 1
    return(myarr:arr)


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



def a2str(myarr:arr, size):
    mystr = string(size)

    i = 0
    while i < size:
        setch(mystr, i, myarr[i])
        i += 1

    return(mystr:str)



# needs to be at bottom, for now https://github.com/ethereum/serpent/issues/44
inset('btcrelay.py')
