# This file is an optimized version of btcTx.py for retrieving
# the first 2 outputs of a Bitcoin transaction.
# It is tested via test_btc-eth.py

# read the VarInt and advance the cursor
macro parseVarInt($txStr, $cursor):
    $arr = getVarintNum($txStr, $cursor)
    $cursor += $arr[0]
    $arr[1]


# return 0 if tx has less than 2 outputs
# or other error, otherwise return array
# of [out1stSatoshis, out1stScriptIndex, out2ndScriptIndex]
def getFirst2Outputs(txStr:str):
    cursor = 4  # skip version

    numIns = parseVarInt(txStr, cursor)
    # log(numIns)
    # log(cursor)

    i = 0
    while i < numIns:
        cursor += 36  # skip prevTxId (32) and outputIndex (4)

        scriptSize = parseVarInt(txStr, cursor)
        cursor += scriptSize + 4  # skip input script and seqNum (4)

        i += 1

    numOuts = parseVarInt(txStr, cursor)
    if numOuts < 2:
        return


    ###########################################################
    # 1st output
    tmpArr = getUInt64LE(txStr, cursor)
    cursor += 8
    out1stSatoshis = tmpArr[1]

    # log(satoshis)

    scriptSize = parseVarInt(txStr, cursor)
    # log(scriptSize)

    if scriptSize == 0:
        return

    out1stScriptIndex = cursor
    cursor += scriptSize + 8  # skip script and 2nd output's satoshis (8)
    ###########################################################



    ###########################################################
    # 2nd output (satoshis were already skipped in previous line)

    scriptSize = parseVarInt(txStr, cursor)
    # log(scriptSize)

    if scriptSize == 0:
        return

    out2ndScriptIndex = cursor
    ###########################################################

    return([out1stSatoshis, out1stScriptIndex, out2ndScriptIndex], items=3)



macro getVarintNum($txStr, $pos):
    $ret = getUInt8($txStr, $pos)
    if $ret == 0xfd:
        $ret = getUInt16LE($txStr, $pos)
    elif $ret == 0xfe:
        $ret = getUInt32LE($txStr, $pos)
    elif $ret == 0xff:
        $ret = getUInt64LE($txStr, $pos)

    $ret

macro getUInt8($txStr, $pos):
    self.getUnsignedBitsLE($txStr, $pos, 8, outitems=2)


macro getUInt16LE($txStr, $pos):
    self.getUnsignedBitsLE($txStr, $pos, 16, outitems=2)


macro getUInt32LE($txStr, $pos):
    self.getUnsignedBitsLE($txStr, $pos, 32, outitems=2)


macro getUInt64LE($txStr, $pos):
    self.getUnsignedBitsLE($txStr, $pos, 64, outitems=2)


# only handles lowercase a-f
def getUnsignedBitsLE(txStr:str, pos, bits):
    size = bits / 4
    offset = pos * 2
    endIndex = offset + size

    result = 0
    j = 0
    while j < size:
        # "01 23 45" want it to read "10 32 54"
        if j % 2 == 0:
            i = j + 1
        else:
            i = j - 1

        char = getch(txStr, i+offset)
        # log(char)
        if (char >= 97 && char <= 102):  # only handles lowercase a-f
            numeric = char - 87
        else:
            numeric = char - 48

        # log(numeric)

        result += numeric * 16^j
        # log(result)

        j += 1

    # need to return size/2 since we don't know the next offset with getVarintNum
    return([size/2, result], items=2)
