extern sampleContractA: [contractA:i]

def callsA(n, x):  # use :a if array
    # m = n[0]
    m = n
    res = x.contractA(m+10, as=sampleContractA)
    return(res)
