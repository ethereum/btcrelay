inset('btcTx.py')

def processTransfer(txStr:str):
    #matches test_2ndTxBlock100K
    # expHashOfOutputScript = 56805804292683358736007883811890392312689386233413306235613681413184995558674
    # res = self.doCheckOutputScript(txStr, len(txStr), 0, expHashOfOutputScript)



    satoshiAndScriptSize = self.parseTransaction(txStr, len(txStr), 0, outitems=2)
    cnt = satoshiAndScriptSize[1] * 2  # note: *2

    numSatoshi = satoshiAndScriptSize[0]

    log(3333)
    log(numSatoshi)

    # TODO using load() until it can be figured out how to use gScript directly with sha256
    myarr = load(self.gScript[0], items=(cnt/32)+1)  # if cnt is say 50, we want 2 chunks of 32bytes
    # log(data=myarr)

    myBtcAddr = text("76a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac")

    res = myarr == myBtcAddr

    return(res)  # expected 1
