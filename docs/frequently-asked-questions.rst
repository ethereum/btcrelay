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


What prevents fees from being too high?
=============================

If a fee for any block header is too high, anyone may
`changeFeeRecipient <https://github.com/ethereum/btcrelay/tree/master#changefeerecipientblockhash-fee-recipient>`_
to themselves.

They can compare the current fee against `getChangeRecipientFee <https://github.com/ethereum/btcrelay/tree/master#getchangerecipientfee>`_
to see if the fee is excessive.  Callers of ``changeFeeRecipient``
must make sure to satisfy all `requirements <https://github.com/ethereum/btcrelay/tree/master#changefeerecipientblockhash-fee-recipient>`_
for successful completion.
