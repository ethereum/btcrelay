inset('btcrelay.py')

def testTargetFromBits():
    bits = 0x19015f53
    exp = 8614444778121073626993210829679478604092861119379437256704
    res = targetFromBits(bits)
    return(res == exp)


def testConcatHash():
    tx1 = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
    tx2 = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
    r = concatHash(tx1, tx2)
    return(r == 0xccdafb73d8dcd0173d5d5c3c9a0770d0b3953db889dab99ef05b1907518cb815)
