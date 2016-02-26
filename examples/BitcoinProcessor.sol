/*
Example contract that can process Bitcoin transactions relayed to it via
BTCRelay.
 */
contract BitcoinProcessor {
    uint256 public lastTxHash;

    address private _trustedBTCRelay;

    function BitcoinProcessor(address trustedBTCRelay) {
        _trustedBTCRelay = trustedBTCRelay;
    }

    // processTransaction should avoid returning the same
    // value as ERR_RELAY_VERIFY (in constants.se) to avoid confusing callers
    //
    // this exact function signature is required as it has to match
    // the signature specified in BTCRelay (otherwise BTCRelay will not call it)
    function processTransaction(bytes txn, uint256 txHash) returns (int256) {
        log0("processTransaction called");

        // only allow trustedBTCRelay, otherwise anyone can provide a fake txn
        if (msg.sender == _trustedBTCRelay) {
            log1("processTransaction txHash, ", bytes32(txHash));
            lastTxHash = txHash;
            // parse & do whatever with txn
            return 1;
        }

        log0("processTransaction failed");
        return 0;
    }
}
