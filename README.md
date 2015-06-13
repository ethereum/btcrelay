# btcrelay

btcrelay is an Ethereum contract for Bitcoin SPV.  The main functionality it provides are:

1. verification of a Bitcoin transaction
1. optionally relay the Bitcoin transaction to any Ethereum contract

### Examples



### API


##### verifyTx(transactionHash, transactionIndex, merkleSibling, blockHash)

Verifies the presence of a transaction on the Bitcoin blockchain, primarily that the transaction is on Bitcoin's main chain and has 6 confirmations.

* `transactionHash` - hash of the transaction, as `int256`
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the hashes of sibling transactions comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`

Returns
* `1` if transaction is verified to be on the Bitcoin blockchain
* `0` otherwise

---

##### relayTx(rawTransaction, transactionHash, transactionIndex, merkleSibling, blockHash, contractAddress)

Verifies a Bitcoin transaction per `verifyTx()` and relays the verified transaction to the specified Ethereum contract.

* `rawTransaction` - hex string of the raw transaction, as `bytes`
* `transactionHash` - hash of the transaction, as `int256`
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the hashes of sibling transactions comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`
* `contractAddress` - address of the Ethereum contract that will receive the verified Bitcoin transaction, as `int256`

The Ethereum contract should have a function of signature `processTransaction(rawTransaction, transactionHash)` and is what will be invoked by `relayTx` if the transaction passes verification.

Returns
* `value` returned by the Ethereum contract's `processTransaction` function
* `0` otherwise



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
