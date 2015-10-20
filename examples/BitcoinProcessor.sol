contract BitcoinProcessor {
    uint256 public lastTxHash;

    function processTransaction(bytes txn, uint256 txHash) returns (int256) {
        log0("processTransaction called");
        log0(bytes32(txHash));
        lastTxHash = txHash;
        // parse & do whatever with txn
        return 1;
    }
}
