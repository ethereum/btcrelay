
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
        self.readSimple(scriptSize, outchars=dblSize)  # return value is ignored

    seqNum = readUInt32LE()
    # log(seqNum)


# returns satoshis, scriptSize and sets self.tmpScriptLen
# TODO eventually, self.tmpScriptLen can probably be removed and also returned by this function
def txoutParse():

    satoshis = readUInt64LE()
    # log(satoshis)

    scriptSize = self.readVarintNum()
    # log(scriptSize)

    if scriptSize > 0:
        self.tmpScriptLen = scriptSize * 2  # self.tmpScriptLen can probably be a return value
        dblSize = self.tmpScriptLen  # needed because compiler complains that save() cannot use self.tmpScriptLen directly
        scriptStr = self.readSimple(scriptSize, outchars=dblSize)
        save(self.gScript[0], scriptStr, chars=dblSize)

    return([satoshis, scriptSize], items=2)


# does not convert to numeric
# make sure caller uses outsz=len*2
def readSimple(len):
    size = len * 2
    offset = self.pos * 2
    endIndex = offset + size

    # TODO ideally, getting a slice of gStr would be done in 1 step, but Serpent limitation
    tmpStr = load(self.gStr[0], chars=endIndex)
    currStr = slice(tmpStr, chars=offset, chars=endIndex)

    self.pos += len # note: len NOT size
    return(currStr:str)



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


# only handles lowercase a-f
# tested via hashBlock()
def stringReadUnsignedBitsLE(inStr:str, bits, pos):
    size = bits / 4
    offset = pos * 2  #TODO remove the *2?
    endIndex = offset + size

    # TODO ideally, getting a slice of gStr would be done in 1 step, but Serpent limitation
    # tmpStr = load(self.gStr[0], chars=endIndex)
    currStr = slice(inStr, chars=offset, chars=endIndex)  #TODO optimize away?

    result = 0
    j = 0
    while j < size:
        # "01 23 45" want it to read "10 32 54"
        if j % 2 == 0:
            i = j + 1
        else:
            i = j - 1

        char = getch(currStr, i)
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
    # self.pos += size / 2

    return(result)


def getBlockVersion(rawBlockHeader:str):
    version = self.stringReadUnsignedBitsLE(rawBlockHeader, 32, 0)
    return(version)

# calls btcrelay hashHeader
def hashBlock(rawBlockHeader:str):
    self.__setupForParsing(rawBlockHeader)

    version = self.stringReadUnsignedBitsLE(rawBlockHeader, 32, 0)
    hashPrevBlock = self.stringReadUnsignedBitsLE(rawBlockHeader, 256, 4)
    hashMerkleRoot = self.stringReadUnsignedBitsLE(rawBlockHeader, 256, 36)
    time = self.stringReadUnsignedBitsLE(rawBlockHeader, 32, 68)
    bits = self.stringReadUnsignedBitsLE(rawBlockHeader, 32, 72)
    nonce = self.stringReadUnsignedBitsLE(rawBlockHeader, 32, 76)

    # version = readUInt32LE()
    # hashPrevBlock = self.readUnsignedBitsLE(256)
    # hashMerkleRoot = self.readUnsignedBitsLE(256)
    # time = readUInt32LE()
    # bits = readUInt32LE()
    # nonce = readUInt32LE()

    res = self.hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(res)

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
    self.__setupForParsing(rawBlockHeader)

    res = self.parseAndStoreHeader(rawBlockHeader)
    return(res)


# heaviestBlock is in btcrelay.py
# def logBlockchainHead():
#     log(self.heaviestBlock)



# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr, and outputScriptSize to self.tmpScriptLen
#
# this is needed until can figure out how a dynamically sized array can be returned from a function
# instead of needing 2 functions, one that returns array size, then calling to get the actual array
# TODO 2nd param size isn't needed anymore
def parseTransaction(rawTx:str, size, outNum):
    self.__setupForParsing(rawTx)
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

    i = 0
    while i < numIns:
        self.txinParse()
        i += 1

    numOuts = self.readVarintNum()

    i = 0
    while i <= outNum:
        satAndSize = self.txoutParse(outsz=2)
        i += 1

    return(satAndSize:arr)


def __setupForParsing(hexStr:str):
    self.pos = 0
    save(self.gStr[0], hexStr, chars=len(hexStr))


def doCheckOutputScript(rawTx:str, size, outNum, expHashOfOutputScript):
    self.parseTransaction(rawTx, size, outNum, outitems=2)  # TODO we are not using the return value, so conceivably self.tmpScriptLen could be returned here and global removed
    cnt = self.tmpScriptLen

    # TODO using load() until it can be figured out how to use gScript directly with sha256
    myarr = load(self.gScript[0], items=(cnt/32)+1)  # if cnt is say 50, we want 2 chunks of 32bytes
    # log(data=myarr)

    hash = sha256(myarr, chars=cnt)  # note: chars=cnt NOT items=...
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

    # TODO ideally, getting a slice of gStr would be done in 1 step, but Serpent limitation
    tmpStr = load(self.gStr[0], chars=endIndex)
    currStr = slice(tmpStr, chars=offset, chars=endIndex)

    result = 0
    j = 0
    while j < size:
        # "01 23 45" want it to read "10 32 54"
        if j % 2 == 0:
            i = j + 1
        else:
            i = j - 1

        char = getch(currStr, i)
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
