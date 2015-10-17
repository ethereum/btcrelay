contract BitcoinProcessor {
    bytes32 public lastTxHash;

    function processTransaction(bytes txn, bytes32 txHash) returns (uint) {
        log0("processTransaction called");
        log0(txHash);
        lastTxHash = txHash;
        // parse & do whatever with txn
        return 1;
    }
}
