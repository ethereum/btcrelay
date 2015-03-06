inset('btcrelay.py')

def bulkStoreHeader(headersBinary:str, count):
    HEADER_SIZE = 80

    offset = 0
    endIndex = HEADER_SIZE

    i = 0
    while i < count:
        currHeader = slice(headersBinary, chars=offset, chars=endIndex)
        res = self.storeBlockHeader(currHeader)

        offset += HEADER_SIZE
        endIndex += HEADER_SIZE
        i += 1

    return(res)
