extern sampleContractA: [processTransfer:s:i]

def callsA(txHex:str, x):
    res = x.processTransfer(txHex)
    return(res)
