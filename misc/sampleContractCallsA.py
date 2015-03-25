extern sampleContractA: [processTransaction:s:i]

def callsA(txHex:str, x):
    res = x.processTransaction(txHex)
    return(res)
