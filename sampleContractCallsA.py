extern sampleContractA: [contractA:i]

def callsA(n):
    x = 0x205215f022af4950618730bcfae161b28397bc41
    res = x.contractA(n+10, as=sampleContractA)
    return(res)
