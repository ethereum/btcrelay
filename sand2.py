data buf[]

data block[2^256](_height, _score, _ancestor[9], _blockHeader[], _prevBlock)

def foo():
    headStr = text("0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710")
    merkleExp = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766

    # save(self.buf[0], headStr, chars=160)
    # tmpStr = load(self.buf[0], chars=160)




    blockHash = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
    hashPrevBlock = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250

    # save ancestors
    self.block[blockHash]._prevBlock = hashPrevBlock
    self.block[blockHash]._height = hashPrevBlock+1# self.block[hashPrevBlock]._height + 1

    self.block[blockHash]._ancestor[0] = hashPrevBlock+2
    i = 1
    while i < 9:
        self.block[blockHash]._ancestor[i] = hashPrevBlock+(2*i)
        i += 1





    save(self.block[blockHash]._blockHeader[0], headStr, chars=160)

    self.block[blockHash]._score = self.block[hashPrevBlock]._score + 0x123456

    tmpStr = load(self.block[blockHash]._blockHeader[0], chars=160)


    gotMerkle = stringReadUnsignedBitsLE(tmpStr, 256, 36)
    log(merkleExp)
    log(gotMerkle)

    return(gotMerkle == merkleExp)




macro stringReadUnsignedBitsLE($inStr, $bits, $pos):
    size = $bits / 4
    offset = $pos * 2  #TODO remove the *2?
    endIndex = offset + size

    result = 0
    exponent = 0
    j = offset
    while j < endIndex:
        # "01 23 45" want it to read "10 32 54"
        if j % 2 == 0:
            i = j + 1
        else:
            i = j - 1

        char = getch($inStr, i)
        # log(char)
        if (char >= 97 && char <= 102):  # only handles lowercase a-f
            numeric = char - 87
        else:
            numeric = char - 48

        # log(numeric)

        result += numeric * 16^exponent
        # log(result)

        j += 1
        exponent += 1

    # return(result)

    result
