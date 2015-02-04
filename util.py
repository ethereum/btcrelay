
# reverses in_arr in pairs, for the purpose of reversing bytes
def pair_rev(in_arr:arr, size):
    if size % 2 != 0:
        return(7777777) # error

    if size == 2:
        return([in_arr[0], in_arr[1]], 2)

    myarr = array(size)
    halfLen = size / 2
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = in_arr[i]
        myarr[i] = in_arr[tailIndex-1]
        myarr[tailIndex-1] = tmp
        tmp = in_arr[i+1]
        myarr[i+1] = in_arr[tailIndex]
        myarr[tailIndex] = tmp
        i += 2
    return(myarr:arr)


# string reverse to array (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def arr_rev(in_arr:arr, size):
    myarr = array(size)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = in_arr[i]
        myarr[i] = in_arr[tailIndex]
        myarr[tailIndex] = tmp
        i += 1
    return(myarr:arr)



# array to int, eg [48,49, 97, 98] -> 0x01ab
# only handles lowercase a-f
def a2int(in_arr:arr):
    size = len(in_arr)
    result = 0
    i = 0
    while i < size:
        char = in_arr[size-1-i]
        # log(char)
        if (char >= 97 && char <= 102):  # only handles lowercase a-f
            numeric = char - 87
        else:
            numeric = char - 48

        # log(numeric)

        result += numeric * 16^i
        # log(result)

        i += 1
    return(result)



# string reverse to array (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def strRev2a(mystring:str, size):
    myarr = array(size)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        tailIndex = size - 1 - i
        tmp = getch(mystring, i)
        myarr[i] = getch(mystring, tailIndex)
        myarr[tailIndex] = tmp
        i += 1
    return(myarr:arr)

    return(b:arr)

# not working yet (since issues such as https://github.com/ethereum/serpent/issues/35 36, 37...)
def str_rev(mystring:str):
    size = len(s)
    halfLen = size / 2
    if size % 2 == 1:
        halfLen += 1
    i = 0
    while i < halfLen:
        oldHead = getch(mystring, i)
        tailIndex = slen - 1 - i
        new = getch(mystring, tailIndex)
        setch(mystring, i, new)
        setch(mystring, tailIndex, oldHead)
        i += 1
    return(mystring:str)


# TESTS

def test_pair_rev_single():
    size = 2
    myarr = array(2)
    myarr[0] = 1
    myarr[1] = 2
    b = self.pair_rev(myarr, size, outsz=size)
    return(b:arr)  # expect [1, 2]

def test_pair_rev():
    size = 4
    myarr = array(4)
    myarr[0] = 1
    myarr[1] = 2
    myarr[2] = 3
    myarr[3] = 4
    b = self.pair_rev(myarr, size, outsz=size)
    return(b:arr)  # expect [3, 4, 1, 2]



def test_arr_rev():
    myarr = array(3)
    myarr[0] = 1
    myarr[1] = 2
    myarr[2] = 3
    b = self.arr_rev(myarr, 3, outsz=3)
    return(b:arr)



def test_a2int():
    myarr = array(4)
    myarr[0] = 48
    myarr[1] = 49
    myarr[2] = 97
    myarr[3] = 98
    res = self.a2int(myarr)
    return(res)

def test_strRev2a():
    mystring = text("abcdef")
    size = len(mystring)
    b = self.strRev2a(mystring, size, outsz=size)


def test_str_rev():
    res = self.str_rev("abc")
    return(res)
    
