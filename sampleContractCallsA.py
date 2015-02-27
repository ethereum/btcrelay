extern sampleContractA: [processTransfer:s:i]

def callsA(x, txHex:str):
    res = x.processTransfer(txHex)
    return(res)
