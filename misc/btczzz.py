# old functions / macros


# calls btcrelay hashHeader
def hashBlock(rawBlockHeader:str):
    version = stringReadUnsignedBitsLE(rawBlockHeader, 32, 0)
    hashPrevBlock = stringReadUnsignedBitsLE(rawBlockHeader, 256, 4)
    hashMerkleRoot = stringReadUnsignedBitsLE(rawBlockHeader, 256, 36)
    time = stringReadUnsignedBitsLE(rawBlockHeader, 32, 68)
    bits = stringReadUnsignedBitsLE(rawBlockHeader, 32, 72)
    nonce = stringReadUnsignedBitsLE(rawBlockHeader, 32, 76)

    # self.__setupForParsing(rawBlockHeader)
    # version = readUInt32LE()
    # hashPrevBlock = self.readUnsignedBitsLE(256)
    # hashMerkleRoot = self.readUnsignedBitsLE(256)
    # time = readUInt32LE()
    # bits = readUInt32LE()
    # nonce = readUInt32LE()

    res = hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
    return(res)

# def isNonceValid(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce):
#     target = targetFromBits(bits)
#
#     hash = hashHeader(version, hashPrevBlock, hashMerkleRoot, time, bits, nonce)
#
#     if lt(hash, target):
#         return(1)
#     else:
#         return(0)


macro hashHeader($version, $hashPrevBlock, $hashMerkleRoot, $time, $bits, $nonce):
    $_version = flipBytes($version, 4)
    $_hashPrevBlock = flipBytes($hashPrevBlock, 32)
    $_hashMerkleRoot = flipBytes($hashMerkleRoot, 32)
    $_time = flipBytes($time, 4)
    $_bits = flipBytes($bits, 4)
    $_nonce = flipBytes($nonce, 4)

    $hash = doRawHashBlockHeader($_version, $_hashPrevBlock, $_hashMerkleRoot, $_time, $_bits, $_nonce)
    $retHash = flipBytes($hash, 32)
    $retHash


macro doRawHashBlockHeader($version, $hashPrevBlock, $hashMerkleRoot, $time, $bits, $nonce):
    verPart = shiftLeftBytes($version, 28)
    hpb28 = shiftRightBytes($hashPrevBlock, 4)  # 81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a3080000
    b1 = verPart | hpb28

    hpbLast4 = shiftLeftBytes($hashPrevBlock, 28)  # 000000000
    hm28 = shiftRightBytes($hashMerkleRoot, 4)  # e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0
    b2 = hpbLast4 | hm28

    hmLast4 = shiftLeftBytes($hashMerkleRoot, 28)
    timePart = ZEROS | shiftLeftBytes($time, 24)
    bitsPart = ZEROS | shiftLeftBytes($bits, 20)
    noncePart = ZEROS | shiftLeftBytes($nonce, 16)
    b3 = hmLast4 | timePart | bitsPart | noncePart

    hash1 = sha256([b1,b2,b3], chars=80)
    hash2 = sha256([hash1], items=1)
    hash2


# eg 0x6162 will be 0x6261
macro flipBytes($n, $numByte):
    $b = byte(31, $n)

    $i = 30
    $j = 1
    while $j < $numByte:
        $b = ($b * 256) | byte($i, $n)
        $i -= 1
        $j += 1

    $b


# shift left bytes
macro shiftLeftBytes($n, $x):
    $n * 256^$x  # set the base to 2 (instead of 256) if we want a macro to shift only bits

# shift right
macro shiftRightBytes($n, $x):
    div($n, 256^$x)
