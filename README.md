# btcrelay

btcrelay is an Ethereum contract for Bitcoin SPV.  The main functionality it provides are:

1. verification of a Bitcoin transaction
1. optionally relay the Bitcoin transaction to any Ethereum contract
1. storage of Bitcoin block headers
1. inspection of the latest Bitcoin block header that is stored

btcrelay is on the Olympic testnet.  Use `web3.eth.namereg.addr('btcrelay')` or run Ethereum JSON-RPC (default port 8545) and click [here](http://cdn.rawgit.com/ethereum/btcrelay/master/examples/relayContractStatus.html)


## API


##### verifyTx(transactionHash, transactionIndex, merkleSibling, blockHash)

Verifies the presence of a transaction on the Bitcoin blockchain, primarily that the transaction is on Bitcoin's main chain and has at least 6 confirmations.

* `transactionHash` - hash of the transaction, as `int256`
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the hashes of sibling transactions comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`

Returns `int256`
* `1` if transaction is verified to be on the Bitcoin blockchain
* `0` otherwise

*Note:* See [examples/sampleCall.html](examples/sampleCall.html) including use of [bitcoin-proof](https://www.npmjs.com/package/bitcoin-proof) for constructing `merkleSibling`.

---

##### relayTx(rawTransaction, transactionHash, transactionIndex, merkleSibling, blockHash, contractAddress)

Verifies a Bitcoin transaction per `verifyTx()` and relays the verified transaction to the specified Ethereum contract.

* `rawTransaction` - hex string of the raw transaction, as `bytes`
* `transactionHash` - hash of the transaction, as `int256`
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the hashes of sibling transactions comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`
* `contractAddress` - address of the Ethereum contract that will receive the verified Bitcoin transaction, as `int256`

The Ethereum contract should have a function of signature `processTransaction(rawTransaction, transactionHash)` and is what will be invoked by `relayTx` if the transaction passes verification.  For an example, see [example-btc-eth](example-btc-eth)

Returns `int256`
* value returned by the Ethereum contract's `processTransaction` function
* `0` otherwise

----

##### storeBlockHeader(blockHeader)

Store a single block header if it is valid, such as a valid Proof-of-Work and the previous block it reference exists.

* `blockHeader` - raw `bytes` of the block header (not the hex string, but the actual bytes).

Returns `int256`
* block height of the header if it was successfully stored
* `0` otherwise


----

##### bulkStoreHeader(bytesOfHeaders, numberOfHeaders)

Store multiple block headers if they are valid.

* `bytesOfHeaders` - raw `bytes` of the block headers (not the hex string, but the actual bytes), with one following immediately the other.
* `numberOfHeaders` - `int256` count of the number of headers being stored.

Returns `int256`
* block height of the last header if all block headers were successfully stored
* `0` if any of the block headers were not successfully stored

*Note:* See [deploy/relayTest/testBulkDeploy.yaml](deploy/relayTest/testBulkDeploy.yaml) for an example of the data for storing multiple headers.  Also, to avoid exceeding Ethereum's block gas limit, a guideline is to store only 5 headers at time.

----

##### getAverageBlockDifficulty()

Returns the difference between the cumulative difficulty of the latest block and the 10th block prior.

This is provided in case an Ethereum contract wants to use the Bitcoin network difficulty as a data feed for some purpose.

----

##### getBlockchainHead(), getLastBlockHeight(), others

`getBlockchainHead` - returns the hash of the latest block, as`int256`

`getLastBlockHeight` - returns the block height of the latest block, as `int256`

See [btcRelayAbi.js](examples/js/btcRelayAbi.js) for other APIs and [relayContractStatus.html](examples/relayContractStatus.html) for an example of calling some of them.

----

## Examples

* [sampleCall.html](examples/sampleCall.html) for calling `verifyTx` including use of [bitcoin-proof](https://www.npmjs.com/package/bitcoin-proof) for constructing `merkleSibling`.

* [example-btc-eth](example-btc-eth) for relaying a Bitcoin transaction to an Ethereum contract using `relayTx`.

* [relayContractStatus.html](examples/relayContractStatus.html) for calling other basic functions.


## Development

Requirements
* [Serpent](https://github.com/ethereum/serpent)
* [pyethereum](https://github.com/ethereum/pyethereum) (for tests)
* [pyepm](https://github.com/etherex/pyepm) (for deployment)

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


## License

[MIT](LICENSE)
