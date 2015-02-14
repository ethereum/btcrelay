data buf[]


def foo():
    headStr = text("0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710")
    merkleExp = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766

    save(self.buf[0], headStr, chars=160)
    tmpStr = load(self.buf[0], chars=160)

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
