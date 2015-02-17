inset('btcTx.py')

BTC_NEED = 5 * 10**8 # satoshis

def processTransfer(txStr:str):
    satoshiAndScriptSize = self.parseTransaction(txStr, len(txStr), 0, outitems=2)
    cnt = satoshiAndScriptSize[1] * 2  # note: *2

    numSatoshi = satoshiAndScriptSize[0]

    log(3333)
    log(numSatoshi)

    # TODO using load() until it can be figured out how to use gScript directly with sha256
    scriptArr = load(self.gScript[0], items=(cnt/32)+1)  # if cnt is say 50, we want 2 chunks of 32bytes
    # log(data=scriptArr)

    myBtcAddr = text("c398efa9c392ba6013c5e04ee729755ef7f58b32")

    #TODO strictly compare the script because an attacker may have a script that mentions
    #our BTC address, but the BTC is not spendable by our private key (only spendable by attacker's key)
    btcWasSentToMe = compareScriptWithAddr(scriptArr, myBtcAddr)



    # 2nd output
    satoshiAndScriptSize = self.parseTransaction(txStr, len(txStr), 1, outitems=2)
    cnt = satoshiAndScriptSize[1] * 2  # note: *2
    scriptArr = load(self.gScript[0], items=(cnt/32)+1)

    ethAddr = getEthAddr(scriptArr, 20, 6)
    log(ethAddr)  # exp 848063048424552597789830156546485564325215747452L

    # expEthAddr = text("948c765a6914d43f2a7ac177da2c2f6b52de3d7c")

    if (btcWasSentToMe && numSatoshi >= BTC_NEED):
        send(ethAddr, 13)
        return(1)


    return(0)


macro getEthAddr($inStr, $size, $offset):
    $endIndex = $offset + ($size * 2)

    $result = 0
    $exponent = 0
    $j = $offset
    while $j < $endIndex:
        $char = getch($inStr, $endIndex-1-$exponent)
        # log($char)

        if ($char >= 97 && $char <= 102):  # only handles lowercase a-f
            $numeric = $char - 87
        else:
            $numeric = $char - 48
        # log($numeric)

        $result += $numeric * 16^$exponent
        # log(result)

        $j += 1
        $exponent += 1

    $result


macro getBEBytes($inStr, $size, $offset):
    div(mload($inStr + $offset), 256**(32 - $size))


macro compareScriptWithAddr($scriptArr, $addrStr):
    $i = 6
    while $i < 26:
        if getch($scriptArr, $i) != getch($addrStr, $i-6):
            $i = 9999 #TODO better way ?
        else:
            $i += 1
    $i == 26
