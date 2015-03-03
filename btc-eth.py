inset('btcSpecialTx.py')

BTC_NEED = 5 * 10**8 # satoshis
MY_BTC_ADDR = text("c398efa9c392ba6013c5e04ee729755ef7f58b32")  # testable with tx[1] from block100K
ETH_TO_SEND = 13

# returns 0 if contract conditions are not met.
# returns the value of send() if they are met (typically send() returns 1 on success)
# callers should probably explicitly check for a return value of 1 for success,
# to protect against the possibility of send() returning non-zero error codes
def processTransfer(txStr:str):
    outputData = self.getFirst2Outputs(txStr, outitems=4)

    if outputData == 0:
        return(0)

    numSatoshi = outputData[0]
    indexScriptOne = outputData[1]

    #TODO strictly compare the script because an attacker may have a script that mentions
    #our BTC address, but the BTC is not spendable by our private key (only spendable by attacker's key)
    btcWasSentToMe = compareScriptWithAddr(indexScriptOne, txStr, MY_BTC_ADDR)


    indexScriptTwo = outputData[2]
    ethAddr = getEthAddr(indexScriptTwo, txStr, 20, 6)
    log(ethAddr)  # exp 848063048424552597789830156546485564325215747452L

    # expEthAddr = text("948c765a6914d43f2a7ac177da2c2f6b52de3d7c")

    if (btcWasSentToMe && numSatoshi >= BTC_NEED):
        res = send(ethAddr, ETH_TO_SEND)
        return(res)

    return(0)


macro getEthAddr($indexStart, $inStr, $size, $offset):
    $endIndex = ($indexStart*2) + $offset + ($size * 2)

    $result = 0
    $exponent = 0
    $j = ($indexStart*2) + $offset
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


macro compareScriptWithAddr($indexStart, $txStr, $addrStr):
    $i = 0
    $j = 6 + ($indexStart * 2)
    while $i < 26:
        if getch($txStr, $j) != getch($addrStr, $i):
            $i = 9999 #TODO better way ?
        else:
            $i += 1
            $j += 1
    $i == 26
