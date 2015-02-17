inset('btcTx.py')


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
