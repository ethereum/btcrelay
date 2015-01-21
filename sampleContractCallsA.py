extern sampleContractA: [contractA:i]

def callsA(n:a, x):
    res = x.contractA(n[0]+10, as=sampleContractA)
    return(res)
