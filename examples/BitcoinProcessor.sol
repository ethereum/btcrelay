contract BitcoinProcessor {
    uint256 public lastTxHash;

    function processTransaction(bytes txn, uint256 txHash) returns (int256) {
        log0("processTransaction called");

        // TODO this is a sample and there should be a check here that msg.sender
        // is the btcrelay contract

        log0(bytes32(txHash));
        lastTxHash = txHash;
        // parse & do whatever with txn
        return 1;
    }
}
