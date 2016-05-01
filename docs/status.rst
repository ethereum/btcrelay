###########################
BTC Relay Status
###########################

***************
Questions
***************

What is shown on the Status page?
=============================

In addition to the address and ABI, the Status shows the latest Bitcoin block
number and blockhash that BTC Relay knows about.  It also shows the very first
Bitcoin block header that is stored by BTC Relay.  BTC Relay can only verify (and
relay) transactions that occur between these blocks.  The Status also shows
the fee for making use of the block header.


What is the ETH fee?
=============================

The amount of wei that needs to be paid to the Relayer when a Bitcoin transaction
belongs in the block.


What is the Relayer?
=============================

The address that will receive the fee.  It is usually the address of the origin
that was first to successfully submit the block header to BTC Relay. 
