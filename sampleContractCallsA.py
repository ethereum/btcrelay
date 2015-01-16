extern sampleContractA: [contractA:i]

def callsA(n, x):
    res = x.contractA(n+10, as=sampleContractA)
    return(res)
