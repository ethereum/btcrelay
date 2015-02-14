inset('btcTx.py')


# def test_parseAndStoreHeader():
#     # from https://en.bitcoin.it/wiki/Block_hashing_algorithm, this is blockheader 125552
#     rawBlockHeader = text("0100000081cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122bc7f5d74df2b9441a42a14695")
#     size = len(rawBlockHeader)
#
#     self.__setupForParsingTx(rawBlockHeader, size)
#     res = self.parseAndStoreHeader(rawBlockHeader)
#     return(res)

# def jtestlog(mystring:str):
#     log(datastr=mystring)


# failing
def testStoreGenesisBlock():
    # genesis
    rawBlockHeader = text("0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c")
    res = self.storeRawBlockHeader(rawBlockHeader, rawBlockHeader)
    return(res)

# failing
def testStoreBlock1():
    # block 1
    rawBlockHeader = text("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299")
    res = self.storeRawBlockHeader(rawBlockHeader, rawBlockHeader)
    return(res)


def testStoringHeaders():
    self.testStoreGenesisBlock()
    res = self.testStoreBlock1()
    return(res)

def testFastHashBlock():
    blockHeaderStr = text("0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710")
    bhBinary = blockHeaderStr
    res = self.fastHashBlock(bhBinary)
    exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
    return(res == exp)

# crashes for some reason TBD
def test_getOutputScript():
    res1 = self.test_getOutput0Script()
    res2 = self.test_getOutput1Script()
    res3 = self.test_getOutputScriptWithMultipleInputs()
    return(res1 == 1 && res2 == 1 && res3 == 1)

def test_getOutputScriptWithMultipleInputs():
    # 3 ins, 2 outs
    rawTx = text("0100000003d64e15b7c11f7532059fe6aacc819b5d886e3aaa602078db57cbae2a8f17cde8000000006b483045022027a176130ebf8bf49fdac27cdc83266a68b19c292b08df1be29f3d964c7e90b602210084ae66b4ff5ed342d78102ef8a4bde87b3ded06929ccaf9a8f71b137baa1816a012102270d473b083897519e5f01c47de7ac50877b6a295775f35966922b3571614370ffffffff54f0e7ded00c01082257eda035d65513b509ddbbe05fae19df0065c294822c9d010000006c493046022100f7423fdbcff22d3cd49921d0af92420d548b925bb1671dc826f15ccc5e05c3de022100d60a6178d892bcf012a79cf9e3430ab70a33b3fa2d156ecf541584e44fa83b150121036674d9607e0461b158c4b3d6368d1869e893cd122c68ebe47af253ff686f064effffffffa6155f8b449da0d3f9d2e1bc8e864c8b78615c1fa560076acaee8802d256a6dd010000006c493046022100e220318b55597c80eecccf9b84f37ab287c14277ccccd269d32f863d8d58d403022100f87818cbed15276f0d5be51aed5bd3b8dea934d6dd2244f2c3170369b96f365501210204b08466f452bb42cefc081ca1c773e26ce0a43566bd9d17b30065c1847072f4ffffffff02301bb50e000000001976a914bdb644fddd802bf7388df220279a18abdf65ebb788ac009ccf6f000000001976a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac00000000")
    outNum = 0
    # exp hash is untested
    expHashOfOutputScript = 56502271141207574289324577080259466406131090189524790551966501267826601078627
    res = self.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
    return(res)

def test_getOutput0Script():
    rawTx = text("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
    outNum = 0
    # exp hash is untested
    expHashOfOutputScript = 15265305399265587892204941549768278966163359751228226364149342078721216369579
    res = self.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
    return(res)

def test_getOutput1Script():
    rawTx = text("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
    outNum = 1
    # exp hash is untested
    expHashOfOutputScript = 115071730706014548547567659794968118611083380235397871058495281758347510448362
    res = self.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
    return(res)


# these tests could be moved to test/test_btcTx.py
# def test_readUInt8_simple():
#     rawTx = text("02")
#     size = len(rawTx)
#     bb = self.str2a(rawTx, size, outsz=size)
#     self.copyToBuf(bb, size)
#
#     self.pos = 0
#     res = readUInt8()
#     exp = 2
#     return(res == exp)
#
# def test_readUInt8():
#     t1 = self.test_readUInt8_simple()
#     t2 = self.test_readUInt8_hex()
#     return(t1 == 1 && t2 == 1)
#
# def test_readUInt8_hex():
#     rawTx = text("3c")
#     size = len(rawTx)
#     bb = self.str2a(rawTx, size, outsz=size)
#     self.copyToBuf(bb, size)
#
#     self.pos = 0
#     res = readUInt8()
#     exp = 60
#     return(res == exp)
#
#
# def test_readUInt16LE_hex():
#     rawTx = text("89ab")
#     save(self.gStr[0], rawTx, chars=len(rawTx))
#     self.pos = 0
#
#     res = readUInt16LE()
#     exp = 0xab89
#     return(res == exp)
#
#
# def test_readUInt32LE():
#     t1 = self.test_readUInt32LE_simple()
#     t2 = self.test_readUInt32LE_hex()
#     t3 = self.test_readUInt32LE_nodejs()
#     return(t1 == 1 && t2 == 1 && t3 == 1)
#
# def test_readUInt32LE_simple():
#     rawTx = text("01000000")
#     size = len(rawTx)
#     bb = self.str2a(rawTx, size, outsz=size)
#     self.copyToBuf(bb, size)
#
#     self.pos = 0
#     res = readUInt32LE()
#     exp = 1
#     return(res == exp)
#
#
# def test_readUInt32LE_hex():
#     # rawTx = text("03042342")
#     rawTx = text("0f000000")
#     size = len(rawTx)
#     bb = self.str2a(rawTx, size, outsz=size)
#     self.copyToBuf(bb, size)
#
#     self.pos = 0
#     res = readUInt32LE()
#     exp = 15
#     return(res == exp)
#
# # test from http://nodejs.org/api/buffer.html#buffer_buf_readuint32le_offset_noassert
# def test_readUInt32LE_nodejs():
#     rawTx = text("03042342")
#     save(self.gStr[0], rawTx, chars=len(rawTx))
#     self.pos = 0
#
#     res = readUInt32LE()
#     exp = 0x42230403
#     return(res == exp)
#
#
#
# def test_readUInt64LE_hex():
#     rawTx = text("abcdef0123456789")
#     size = len(rawTx)
#     bb = self.str2a(rawTx, size, outsz=size)
#     self.copyToBuf(bb, size)
#
#     self.pos = 0
#     res = readUInt64LE()
#     exp = 0x8967452301efcdab
#     return(res == exp)
#
#
#
# def test_str2a():
#     mystring = text("abcdef")
#     size = len(mystring)
#     b = self.str2a(mystring, size, outsz=size)
#     return(b:arr)
#
# def test_initFromBuf():
#     size = 3
#     self.buf[0] = 1
#     self.buf[1] = 3
#     self.buf[2] = 5
#     bb = self.initFromBuf(size, outsz=size)
#     return(bb:arr)
#
# def test_a2str():
#     # mystr = text("cow")
#     # log(datastr=mystr)
#
#     myarr = array(3)
#     myarr[0] = 99
#     myarr[1] = 111
#     myarr[2] = 119
#
#     mystr = self.a2str(myarr, 3, outsz=3)
#     log(datastr=mystr)
