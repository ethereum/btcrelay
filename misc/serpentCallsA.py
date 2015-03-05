extern sampleContractA: [contractA:i]

def test(x, arr:a):
    # SAMPLEA = create('sampleContractA.py')
    # p10 = 9997

    p10 = arr[0] + 10
    # res = SAMPLEA.contractA(p10, as=sampleContractA)
    res = x.contractA(p10, as=sampleContractA)
    return(res)


#
# extern mul2: [double]
#
# MUL2 = create('mul2.se')
# return(MUL2.double(5, as=mul2))
