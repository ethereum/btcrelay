inset('../btcrelay.py')

# test only method required by some tests
def testingonlySetHeaviest(blockHash):
    self.heaviestBlock = blockHash



#
# macro wrappers (since only functions are testable)
#

def funcTargetFromBits(bits):
    return(targetFromBits(bits))

def funcConcatHash(tx1, tx2):
    return(concatHash(tx1, tx2))

#
# end of macro wrappers
#
