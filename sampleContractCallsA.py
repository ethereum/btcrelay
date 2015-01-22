extern sampleContractA: [contractA:i]

def callsA(x, n:a):  # use :a if array
    # m = n[0]
    # p10 = m + 10
    # m = n

    p10 = 9997
    res = x.contractA(p10, as=sampleContractA)
    return(res)
