inset('btcrelay.py')

# store 'count' number of Bitcoin blockheaders represented as one
# continuous 'headersBinary' (which should have length 80*count
# since a single Bitcoin block header is 80 bytes)
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
