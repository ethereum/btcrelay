
def a2str(myarr:arr, size):
    mystr = string(size)

    i = 0
    while i < size:
        setch(mystr, i, myarr[i])
        i += 1

    return(mystr:str)

def str2a(mystring:str, size):
    myarr = array(size)
    i = 0
    while i < size:
        myarr[i] = getch(mystring, i)
        i += 1
    return(myarr:arr)
    
def test():
    # mystr = text("cow")
    # log(datastr=mystr)

    scriptStr = text("76a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac")

    size = len(scriptStr)

    myarr = self.str2a(scriptStr, size, outsz=size)

    # myarr = array(3)
    # myarr[0] = 99
    # myarr[1] = 111
    # myarr[2] = 119

    mystr = self.a2str(myarr, size, outsz=size)
    log(datastr=mystr)

    # log(data=myarr) has extra 0s which is expected


    # mystr = string(96)
    # mcopy(mystr, myarr, items=3)
    # log(datastr=mystr)


    #
    # mcopy(mystr, myarr, chars=3)
    # log(datastr=mystr)
    #
    # mcopy(mystr, myarr, 3)
    # log(datastr=mystr)


    # mystr = text("cow")
    # h = sha3(mystr, chars=3)
    # log(h)
    # return(h)
