
# contains the string to be deserialized/parse (currently a tx or blockheader)
data gStr[]

# index to gStr
data pos

# contains a script, currently only used for outputScripts since input scripts are ignored
data gScript[]

# used by getFirst2Outputs, for storing the 2nd script of a txoutput
data g2ndScript[]


def txinParse():
    prevTxId = self.readUnsignedBitsLE(256)
    outputIndex = readUInt32LE()
    # log(outputIndex)

    scriptSize = readVarintNum()

    if scriptSize > 0:
        dblSize = scriptSize*2
        self.readSimple(scriptSize, outchars=dblSize)  # return value is ignored

    seqNum = readUInt32LE()
    # log(seqNum)


# returns satoshis, scriptSize
def txoutParse():

    satoshis = readUInt64LE()
    # log(satoshis)

    scriptSize = readVarintNum()
    # log(scriptSize)

    if scriptSize > 0:
        dblSize = scriptSize * 2
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



macro readVarintNum():
    $ret = readUInt8()
    if $ret == 0xfd:
        $ret = readUInt16LE()
    elif $ret == 0xfe:
        $ret = readUInt32LE()
    elif $ret == 0xff:
        $ret = readUInt64LE()

    $ret


# heaviestBlock is in btcrelay.py
# def logBlockchainHead():
#     log(self.heaviestBlock)



# precondition: __setupForParsing() has been called
# returns an array [satoshis, outputScriptSize] and writes the
# outputScript to self.tmpScriptArr
def __getMetaForOutput(outNum):
    version = readUInt32LE()
    # log(version)
    # log(self.pos)
    numIns = readVarintNum()
    # log(numIns)
    # log(self.pos)

    i = 0
    while i < numIns:
        self.txinParse()
        i += 1

    numOuts = readVarintNum()

    i = 0
    while i <= outNum:
        satAndSize = self.txoutParse(outsz=2)
        i += 1

    return(satAndSize:arr)


# return 0 if tx has less than 2 outputs
# or other error, otherwise return array
# of [out1stSatoshis, out1stScriptSize, out2ndScriptSize]
def getFirst2Outputs(txStr:str):
    __setupForParsing(txStr)

    self.pos += 4  # skip version

    numIns = readVarintNum()
    # log(numIns)
    # log(self.pos)

    i = 0
    while i < numIns:
        self.pos += 32  # skip prevTxId
        self.pos += 4  # skip outputIndex

        scriptSize = readVarintNum()
        self.pos += scriptSize # skip reading the input scripts

        self.pos += 4  # skip seqNum

        i += 1

    numOuts = readVarintNum()
    if numOuts < 2:
        return(0)


    ###########################################################
    # 1st output
    out1stSatoshis = readUInt64LE()
    # log(satoshis)

    scriptSize = readVarintNum()
    # log(scriptSize)

    if scriptSize == 0:
        return(0)


    indexScriptOne = self.pos
    self.pos += scriptSize  # script can be skipped since we return the index to it
    out1stScriptSize = scriptSize
    ###########################################################



    ###########################################################
    # 2nd output
    self.pos += 8  # skip satoshis

    scriptSize = readVarintNum()
    # log(scriptSize)

    if scriptSize == 0:
        return(0)

    dblSize = scriptSize * 2
    scriptStr = self.readSimple(scriptSize, outchars=dblSize)
    save(self.g2ndScript[0], scriptStr, chars=dblSize)  # note: g2ndScript

    out2ndScriptSize = scriptSize
    ###########################################################

    return([out1stSatoshis, out1stScriptSize, out2ndScriptSize, indexScriptOne], items=4)


# general function for getting a tx output; for something faster and
# explicit, see getFirst2Outputs()
#
# this is needed until can figure out how a dynamically sized array can be
# returned from a function instead of needing 2 functions, one that
# returns array size, then calling to get the actual array
def parseTransaction(rawTx:str, outNum):
    __setupForParsing(rawTx)
    meta = self.__getMetaForOutput(outNum, outsz=2)
    return(meta, items=2)


macro __setupForParsing($hexStr):
    self.pos = 0  # important
    save(self.gStr[0], $hexStr, chars=len($hexStr))


def doCheckOutputScript(rawTx:str, size, outNum, expHashOfOutputScript):
    satoshiAndScriptSize = self.parseTransaction(rawTx, outNum, outitems=2)
    cnt = satoshiAndScriptSize[1] * 2  # note: *2

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
