inset('btcrelay.py')

def bulkStoreHeader(headersBinary:str, count):
    HEADER_SIZE = 80

    offset = 0
    endIndex = HEADER_SIZE

    i = 0
    while i < count:
        currHeader = slice(headersBinary, chars=offset, chars=endIndex)
        res = self.storeBlockHeader(currHeader)
        if res != 2 + i:
            log(111111111111111222222222222222)
            return(0)

        offset += HEADER_SIZE
        endIndex += HEADER_SIZE
        i += 1

    return(res)
