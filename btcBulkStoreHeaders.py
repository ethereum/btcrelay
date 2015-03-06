inset('btcrelay.py')

def bulkStoreHeader(headersBinary:str):
    HEADER_SIZE = 80

    offset = 0
    endIndex = HEADER_SIZE
    currHeader = slice(headersBinary, chars=offset, chars=endIndex)
    log(444444444)
    log(datastr=currHeader)

    offset += HEADER_SIZE
    endIndex += HEADER_SIZE
    currHeader = slice(headersBinary, chars=offset, chars=endIndex)
    log(55)
    log(datastr=currHeader)


    # self.storeBlockHeader
