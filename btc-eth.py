inset('btcSpecialTx.py')

data owner
data trustedBtcRelay
data btcAcceptAddr

# records txs that have successfully claimed Ether (thus not allowed to re-claim)
data txClaim[2^256]


# TODO remove when not testing, since owners should create another copy of this
# contract if they want to get paid to a different btcAddr
def testingonlySetBtcAddr(btcAddr):
    if msg.sender == self.owner:
        self.btcAcceptAddr = btcAddr
        return(1)
    return(0)

def shared():
    BTC_NEED = 5 * 10**8 # satoshis
    MY_BTC_ADDR = 0xc398efa9c392ba6013c5e04ee729755ef7f58b32  # testable with tx[1] from block100K
    ETH_TO_SEND = 13  # wei

def init():
    self.owner = msg.sender
    self.btcAcceptAddr = MY_BTC_ADDR

# trustedRelayContract is the address of the trusted btcrelay contract
def setTrustedBtcRelay(trustedRelayContract):
    if msg.sender == self.owner:
        self.trustedBtcRelay = trustedRelayContract
        return(1)
    return(0)


# returns 0 if contract conditions are not met.
# returns the value of send() if they are met (typically send() returns 1 on success)
# callers should probably explicitly check for a return value of 1 for success,
# to protect against the possibility of send() returning non-zero error codes
def processTransfer(txStr:str, txHash):
    # apart from trustedBtcRelay, only the owner may claim ether
    if msg.sender != self.trustedBtcRelay:
        if tx.origin != self.owner:  # tx.origin is superset of msg.sender, so no need for checking msg.sender==self.owner
            return(0)

    # only the owner may reclaim; trustedBtcRelay and others can NOT reclaim
    if self.txClaim[txHash] != 0:
        if tx.origin != self.owner:  # allow owner to keep reclaiming (helpful in testing)
            return(0)

    outputData = self.getFirst2Outputs(txStr, outitems=3)

    if outputData == 0:
        return(0)

    numSatoshi = outputData[0]
    indexScriptOne = outputData[1]

    #TODO strictly compare the script because an attacker may have a script that mentions
    #our BTC address, but the BTC is not spendable by our private key (only spendable by attacker's key)
    # btcWasSentToMe = compareScriptWithAddr(indexScriptOne, txStr, self.btcAcceptAddr)
    addrBtcWasSentTo = getEthAddr(indexScriptOne, txStr, 20, 6)

    btcWasSentToMe = addrBtcWasSentTo == self.btcAcceptAddr


    indexScriptTwo = outputData[2]
    ethAddr = getEthAddr(indexScriptTwo, txStr, 20, 6)
    # log(ethAddr)  # exp 848063048424552597789830156546485564325215747452L

    # expEthAddr = text("948c765a6914d43f2a7ac177da2c2f6b52de3d7c")

    if (btcWasSentToMe && numSatoshi >= BTC_NEED):
        res = send(ethAddr, ETH_TO_SEND)
        self.txClaim[txHash] = res
        log(msg.sender, data=[res])
        return(res)

    return(0)


def setOwner(newOwner):
    if msg.sender == self.owner:
        self.owner = newOwner
        return(1)
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



macro compareScriptWithStringAddr($indexStart, $txStr, $addrStr):
    $i = 0
    $j = 6 + ($indexStart * 2)
    while $i < 26:
        if getch($txStr, $j) != getch($addrStr, $i):
            $i = 9999 #TODO better way ?
        else:
            $i += 1
            $j += 1
    $i == 26
