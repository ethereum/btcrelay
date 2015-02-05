
# contains the string to be deserialized/parse (currently a tx or blockheader)
data gStr[]

# index to gStr
data pos

# contains a script, currently only used for outputScripts since input scripts are ignored
data gScript[]

# length of gScript
data tmpScriptLen


def txinParse():
    prevTxId = self.readUnsignedBitsLE(256)
    outputIndex = readUInt32LE()
    # log(outputIndex)

    scriptSize = self.readVarintNum()

    if scriptSize > 0:
        dblSize = scriptSize*2
        self.readSimple(scriptSize, outsz=dblSize)  # return value is ignored

    seqNum = readUInt32LE()
    # log(seqNum)


# returns satoshis, scriptSize and sets self.tmpScriptLen
# eventually, self.tmpScriptLen can probably be removed and also returned by this function
def txoutParse():

    satoshis = readUInt64LE()
    # log(satoshis)

    scriptSize = self.readVarintNum()
    # log(scriptSize)

    if scriptSize > 0:
        self.tmpScriptLen = scriptSize * 2  # self.tmpScriptLen can probably be a return value
        dblSize = self.tmpScriptLen  # needed because compiler complains that save() cannot use self.tmpScriptLen directly
        scriptStr = self.readSimple(scriptSize, outsz=dblSize)
        save(self.gScript[0], scriptStr, chars=dblSize)

    return([satoshis, scriptSize], items=2)


# does not convert to numeric
# make sure caller uses outsz=len*2
def readSimple(len):
    size = len * 2
    offset = self.pos * 2
    endIndex = offset + size

    jstr = load(self.gStr[0], chars=endIndex)

    log(90011)
    log(datastr=jstr)

    currStr = slice(jstr, chars=offset, chars=endIndex)
    log(903333333333333)
    self.pos += len # note: len NOT size
    # log(data=bb)
    # return(bb:arr)
    log(datastr=currStr)
    return(currStr:str)



# tested via twip()
def readVarintNum():
    first = readUInt8()
    if first == 0xfd:
        return(readUInt16LE())
    elif first == 0xfe:
        return(readUInt32LE())
    elif first == 0xff:
        return(readUInt64LE())
    else:
        return(first)


def callBtcRelayToStoreHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
    res = self.storeBlockHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(res)


def parseAndStoreHeader(rawHeader:str):
    version = readUInt32LE()
    prevHash = self.readUnsignedBitsLE(256)
    merkleRoot = self.readUnsignedBitsLE(256)
    time = readUInt32LE()
    bits = readUInt32LE()
    nonce = readUInt32LE()

    # log(version)
    # log(merkleRoot)

    res = self.callBtcRelayToStoreHeader(version, prevHash, merkleRoot, time, bits, nonce)
    return(res)



def storeRawBlockHeader(rawBlockHeader:str):
    # size = len(rawBlockHeader)

    self.pos = 0
    save(self.gStr[0], rawBlockHeader, chars=len(rawBlockHeader))

    # self.__setupForParsingTx(rawBlockHeader, size)

    res = self.parseAndStoreHeader(rawBlockHeader)
    return(res)


# heaviestBlock is in btcrelay.py
def logBlockchainHead():
    log(self.heaviestBlock)



# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr, and outputScriptSize to self.tmpScriptLen
#
# this is needed until can figure out how a dynamically sized array can be returned from a function
# instead of needing 2 functions, one that returns array size, then calling to get the actual array
def parseTransaction(rawTx:str, size, outNum):
    self.__setupForParsingTx(rawTx, size)
    meta = self.__getMetaForOutput(outNum, outsz=2)
    return(meta, items=2)



# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr, and outputScriptSize to self.tmpScriptLen
def __getMetaForOutput(outNum):
    version = readUInt32LE()
    # log(version)
    # log(self.pos)
    numIns = self.readVarintNum()
    # log(numIns)
    # log(self.pos)

    log(44)

    i = 0
    while i < numIns:
        self.txinParse()
        i += 1

    log(555)

    numOuts = self.readVarintNum()
    log(numOuts)

    i = 0
    while i <= outNum:
        satAndSize = self.txoutParse(outsz=2)
        i += 1

    log(899)

    return(satAndSize:arr)


def __setupForParsingTx(hexStr:str, size):
    self.pos = 0
    save(self.gStr[0], hexStr, chars=len(hexStr))


def doCheckOutputScript(rawTx:str, size, outNum, expHashOfOutputScript):
    self.parseTransaction(rawTx, size, outNum)

    # scriptStr = self.a2str(scriptArr, self.tmpScriptLen, outsz=self.tmpScriptLen)
    # log(datastr=scriptStr)

    log(3232)
    cnt = self.tmpScriptLen
    log(cnt)
    # log(self.tmpScriptLen)

    b=byte(0, self.gScript[0])
    log(b)
    b=byte(1, self.gScript[0])
    log(b)
    b=byte(2, self.gScript[0])
    log(b)
    b=byte(3, self.gScript[0])
    log(b)

    myarr = load(self.gScript[0], items=(cnt/32)+1)
    log(data=myarr)

    hash = sha256(myarr, chars=cnt)

    # hash = sha256(self.gScript[0], items=cnt)
    log(4343)
    # log(hash)
    return(hash == expHashOfOutputScript)


# this may not be needed so holding off on it
# returns an array
# [ version, numIns, ins[ [prevTx, outputIndex, scriptSize, script, seqNumber] ],
# numOuts, outs[ [satoshis, scriptSize, script] ], locktime ]
# def deserialize():



# only handles lowercase a-f
# tested via tests for readUInt8, readUInt32LE, ...
def readUnsignedBitsLE(bits):
    size = bits / 4
    offset = self.pos * 2
    endIndex = offset + size

    jstr = load(self.gStr[0], chars=endIndex)

    currStr = slice(jstr, chars=offset, chars=endIndex)

    result = 0
    j = 0
    while j < size:
        # "01 23 45" want it to read "10 32 54"
        if j % 2 == 0:
            i = j + 1
        else:
            i = j - 1

        # log(1000+i)
        char = getch(currStr, i) # self.buf[offset + i]
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

macro readUInt8():
    self.readUnsignedBitsLE(8)


macro readUInt16LE():
    self.readUnsignedBitsLE(16)


# only handles lowercase a-f
macro readUInt32LE():
    self.readUnsignedBitsLE(32)


macro readUInt64LE():
    self.readUnsignedBitsLE(64)



# needs to be at bottom, for now https://github.com/ethereum/serpent/issues/44
inset('btcrelay.py')
