contract BitcoinProcessor {
    uint256 public lastTxHash;

    address private _trustedBTCRelay;

    function BitcoinProcessor(address trustedBTCRelay) {
        _trustedBTCRelay = trustedBTCRelay;
    }

    function processTransaction(bytes txn, uint256 txHash) returns (int256) {
        log0("processTransaction called");

        // only allow trustedBTCRelay, otherwise anyone can provide a
        // fake txn
        if (msg.sender == _trustedBTCRelay) {
            log1("processTransaction tHash, ", bytes32(txHash));
            // log0(bytes32(txHash));
            lastTxHash = txHash;
            // parse & do whatever with txn
            return 1;
        }

        log0("processTransaction failed");
        return 0;
    }
}
