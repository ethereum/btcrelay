contract MockBTCRelay {
    function storeBlockHeader(bytes blockHeaderBytes) returns(int256) {
        return -2;
    }

    function storeBlockWithFee(bytes blockHeaderBytes, int256 fee) returns(int256) {
        return -3;
    }
}

contract HeaderSubmitter {
    MockBTCRelay mock;

    // rejects payments
    function() {
        throw;
    }

    function storeHeader(bytes header, address btcrelayAddr) returns(int256) {
        mock = MockBTCRelay(btcrelayAddr);
        return mock.storeBlockHeader(header);
    }

    function storeHeaderWithFee(bytes header, int256 fee, address btcrelayAddr) returns(int256) {
        mock = MockBTCRelay(btcrelayAddr);
        return mock.storeBlockWithFee(header, fee);
    }
}
