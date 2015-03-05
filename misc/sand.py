
data buf[]


def foo():
    # mystr = text("1")
    # res = sha256(mystr:str)
    # return(res)


    mystr = text("11111111111111111111111111111111")
    save(self.buf[0], mystr, chars=32)

    myarr = load(self.buf[0], items=1)
    log(data=myarr)

    res = sha256(myarr, chars=1)
    return(res)



    # self.buf[0] = 1
    # self.buf[1] = 3
    # self.buf[2] = 5
    #
    # myarr = array(3)
    # mcopy(myarr, self.buf[0], chars=3)
    # return(myarr:arr)



    # myarr = load(self.buf[0], items=3):arr
    # return(myarr:arr)

    # return(load(self.buf[0], chars=3):arr)






    # mystr=text("81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b")
    # save(self.buf[0], mystr, chars=len(mystr))
    #
    # self.g()


# mystr = text("0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b")

# mystr=text("01ab00")


    # log(mystr[0])
    # log(mystr[2])
    # log(mystr[4])
    # log(mystr[6])
    #
    #
    # b = byte(0, mystr[0])
    # log(b)
    #
    # b = byte(0, mystr[2])
    # log(b)
    #
    # b = byte(0, mystr[4])
    # log(b)
    #
    # b = byte(0, mystr[6])
    # log(b)



# def g():
#     jstr = load(self.buf[0], chars=132)
#     log(datastr=jstr)
#
#     j = slice(jstr, chars=128, chars=132)
#     log(datastr=j)

    # log(self.buf[0])



    # j = slice(mystr, chars=128, chars=132)
    #
    # log(datastr=j)
    # log(j)

    # b = byte(2, self.buf[0])
    # log(b)

    # log(datastr=self.buf[0])
    #
    # log(self.buf[0])
    # log(self.buf[1])
    # log(self.buf[4])
    # log(self.buf[6])


# data buf
#
# def foo():
#     mystr = text("01ab")
#     mcopy(self.buf, mystr, chars=4)
#
#     # self.buf = mystr
#
#
#
#     log(datastr=self.buf)
#     self.g()
#
# def g():
#     log(datastr=self.buf)




    # mystr = text("01ab")
    # save(self.buf[0], mystr, chars=4)
    # log(self.buf[0])
    # log(self.buf[1])
    # return(load(self.buf[0], chars=4):arr)


    # log(data=self.buf[0])

    # save(self.buf, mystr:str)
    # log(datastr=self.buf)

    # log(self.buf[0])
    # log(self.buf[2])
    # return(load(self.buf[0], chars=4):str)  # tried offset 1 to try getting 2nd and 3rd elements
    #
    #
    #
    # return(self.buf[1])


# def init():
#     self.buf[0] = 5
#     self.buf[1] = 6
#     self.buf[2] = 7
