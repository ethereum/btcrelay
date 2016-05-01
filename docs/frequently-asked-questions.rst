###########################
Frequently Asked Questions
###########################

How to use BTC Relay?
=============================

Did you see `How to use BTC Relay? <https://github.com/ethereum/btcrelay/tree/master#how-to-use-btc-relay>`_


Why isn't verifyTx / relayTx working?
=============================

* Does your transaction have at least 6 Bitcoin confirmations?

* Did you pass the correct parameters to
  `construct the Merkle proof <https://www.npmjs.com/package/bitcoin-proof>`_ correctly?
  Viewing the page source of the `examples <https://github.com/ethereum/btcrelay/tree/master#examples>`_
  might help.

* Did you send at least the fee as indicated by `getFeeAmount <https://github.com/ethereum/btcrelay/tree/master#getfeeamountblockhash>`_?
