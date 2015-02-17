inset('btcTx.py')

def processTransfer(txStr:str):
    #matches test_2ndTxBlock100K
    expHashOfOutputScript = 56805804292683358736007883811890392312689386233413306235613681413184995558674

    res = self.doCheckOutputScript(txStr, len(txStr), 0, expHashOfOutputScript)

    return(res)  # expected 1
