# [BTC Relay](http://btcrelay.org)

[![Join the chat at https://gitter.im/ethereum/btcrelay](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ethereum/btcrelay)

[BTC Relay](http://btcrelay.org) is an Ethereum contract for Bitcoin SPV.  The main functionality it provides are:

1. verification of a Bitcoin transaction
1. optionally relay the Bitcoin transaction to any Ethereum contract
1. storage of Bitcoin block headers
1. inspection of the latest Bitcoin block header that is stored

BTC Relay is [live](http://rawgit.com/ethereum/btcrelay/master/examples/relayContractStatus.html) on the testnet.


## API


##### verifyTx(rawTransaction, transactionIndex, merkleSibling, blockHash)

Verifies the presence of a transaction on the Bitcoin blockchain, primarily that the transaction is on Bitcoin's main chain and has at least 6 confirmations.

* `rawTransaction` - raw `bytes` of the transaction
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the sibling hashes comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`

Returns `uint256`
* hash of the verified Bitcoin transaction
* `0` if `rawTransaction` is exactly 64 bytes in length or fails verification

*Note:* See [examples/sampleCall.html](examples/sampleCall.html) including use of [bitcoin-proof](https://www.npmjs.com/package/bitcoin-proof) for constructing `merkleSibling`.

---

##### relayTx(rawTransaction, transactionIndex, merkleSibling, blockHash, contractAddress)

Verifies a Bitcoin transaction per `verifyTx()` and relays the verified transaction to the specified Ethereum contract.

* `rawTransaction` - raw `bytes` of the transaction
* `transactionIndex` - transaction's index within the block, as `int256`
* `merkleSibling` - array of the sibling hashes comprising the Merkle proof, as `int256[]`
* `blockHash` - hash of the block that contains the transaction, as `int256`
* `contractAddress` - address of the processor contract that will receive the verified Bitcoin transaction, as `int256`

The processor contract at `contractAddress` should have a function of signature
`processTransaction(bytes rawTransaction, uint256 transactionHash) returns (int256)`
and is what will be invoked by `relayTx` if the transaction passes
verification.  For examples, see
[BitcoinProcessor.sol](examples/BitcoinProcessor.sol)
and [example-btc-eth](example-btc-eth).

Returns `int256`
* value returned by the processor contract's `processTransaction` function
* or ERR_RELAY_VERIFY, see [constants.se](constants.se)

Note: Callers cannot be 100% certain when an ERR_RELAY_VERIFY occurs because
it may also have been returned by processTransaction().  Callers should be
aware of the contract that they are relaying transactions to, and
understand what the processor contract's processTransaction method returns.

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

##### getBlockHeader(blockHash)

Get the 80 byte block header for a given `blockHash`.  A payment value of
`getFeeAmount(blockHash)` must be provided in the transaction.

* `blockHash` - hash of the block as `int256`

Returns `bytes`
* block header, always as 80 bytes (all zeros if header does not exist)
* or `0` (as a single byte) if insufficient payment is provided

----

##### getBlockHash(blockHeight)

Get the block hash for a given `blockHeight`.

* `blockHeight` - height of the block as `int256`.  Minimum value is `1`.

Returns `int256`
* block hash
* `0` if not found

----

##### getAverageChainWork()

Returns the difference between the chainWork of the latest block and the
10th block prior.

This is provided in case an Ethereum contract wants to use the chainWork
or Bitcoin network difficulty (which can be derived) as a data feed.

----

##### getBlockchainHead(), getLastBlockHeight(), others

`getBlockchainHead` - returns the hash of the latest block, as`int256`

`getLastBlockHeight` - returns the block height of the latest block, as `int256`

See [BitcoinRelayAbi.js](examples/BitcoinRelayABI.js) for other APIs and [relayContractStatus.html](examples/relayContractStatus.html) for an example of calling some of them.

----

##### Incentives

The following APIs are described in `Incentives for Relayers` below.

`storeBlockWithFee()`, `changeFeeRecipient()`, `getFeeRecipient()`, `getFeeAmount()`, `getChangeRecipientFee()`

----

## Examples

* [sampleCall.html](examples/sampleCall.html) for calling `verifyTx` including use of [bitcoin-proof](https://www.npmjs.com/package/bitcoin-proof) for constructing `merkleSibling`.

* [example-btc-eth](example-btc-eth) for relaying a Bitcoin transaction to an Ethereum contract using `relayTx`.

* [relayContractStatus.html](examples/relayContractStatus.html) for calling other basic functions.

----

## Incentives for Relayers

Relayers are those who submit block headers to BTC Relay.  To incentivize the community
to be relayers, and thus allow BTC Relay to be autonomous and up-to-date with the
Bitcoin blockchain, Relayers can call `storeBlockWithFee`.  The Relayer will be the
`getFeeRecipient()` for the block they submit, and when any transactions are verified
in the block, or the header is retrieved via `getBlockHeader`, the Relayer will be
 rewarded with `getFeeAmount()`.

To avoid a relayer R1 from setting excessing fees, it is possible for a relayer R2
to `changeFeeRecipient()`.  R2 must specify a fee lower than what R1 specified, and
pay `getChangeRecipientFee()` to R1, but now R2 will be the `getFeeRecipient()` for the block
and will earn all future `getFeeAmount()`.

With this background, here are API details for incentives.

##### storeBlockWithFee(blockHeader, fee)

Store a single block header (like `storeBlockHeader`) and
set a fee that will be charged for verifications that use `blockHeader`.

* `blockHeader` - raw `bytes` of the block header (not the hex string, but the actual bytes).
* `fee` - `int256` amount in wei.

Returns `int256`
* block height of the header if it was successfully stored
* `0` otherwise

----

##### changeFeeRecipient(blockHash, fee, recipient)

Set the `fee` and `recipient` for a given `blockHash`.  The call must have `msg.value`
of at least `getChangeRecipientFee()`, and must also specify a `fee` lower than
the current `getFeeAmount(blockHash)`.

* `blockHash` - hash of the block as `int256`.
* `fee` - `int256` amount in wei.
* `recipient` - `int256` address of the recipient of fees.

Returns `int256`
* `1` if the fee and recipient were successfully set
* `0` otherwise

----

##### getFeeRecipient(blockHash)

Get the address that receives the fees for a given `blockHash`.

* `blockHash` - hash of the block as `int256`.

Returns `int256`
* address of the recipient

----

##### getFeeAmount(blockHash)

Get the fee amount in wei for verifications using a given `blockHash`.

* `blockHash` - hash of the block as `int256`.

Returns `int256`
* amount of the fee in wei.

----

##### getChangeRecipientFee()

Get the amount of wei required that must be sent to BTC Relay when calling
`changeFeeRecipient`.

Returns `int256`
* amount of wei

----

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

See [full MIT License](LICENSE) including:
```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
