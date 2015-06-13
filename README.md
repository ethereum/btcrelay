# btcrelay

btcrelay is an Ethereum contract for Bitcoin SPV.  The main functionality it provides are:

1. verification of a Bitcoin transaction
1. optionally relay the Bitcoin transaction to any Ethereum contract

### Examples



### API


##### verifyTx(transactionHash, transactionIndex, merkleSibling, blockHash)

* `transactionHash` - hash of the transaction, as `int256`
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the hashes of sibling transactions comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`

int256,int256,int256[],int256)


##### relayTx(bytes,int256,int256,int256[],int256,int256)



Requirements
------------
* [Serpent](https://github.com/ethereum/serpent)
* [pyethereum](https://github.com/ethereum/pyethereum) Python Ethereum (needed to run tests)


#### Running tests

Exclude slow tests:
```
py.test test/ -s -m "not slow"
```

Run slow tests without veryslow tests
```
py.test test/ -s -m "slow and not veryslow"
```

All tests:
```
py.test test/ -s
```
