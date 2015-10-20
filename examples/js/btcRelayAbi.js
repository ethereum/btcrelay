<<<<<<< HEAD
window.btcRelayAbi = [{
    "name": "bulkStoreHeader(bytes,int256)",
    "type": "function",
    "inputs": [{ "name": "headersBytes", "type": "bytes" }, { "name": "count", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "computeMerkle(int256,int256,int256[])",
    "type": "function",
    "inputs": [{ "name": "txHash", "type": "int256" }, { "name": "txIndex", "type": "int256" }, { "name": "sibling", "type": "int256[]" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "getAverageBlockDifficulty()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "getBlockchainHead()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "getCumulativeDifficulty()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "getLastBlockHeight()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "inMainChain(int256)",
    "type": "function",
    "inputs": [{ "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "relayTx(bytes,int256,int256,int256[],int256,int256)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "bytes" }, { "name": "txHash", "type": "int256" }, { "name": "txIndex", "type": "int256" }, { "name": "sibling", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }, { "name": "contract", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "storeBlockHeader(bytes)",
    "type": "function",
    "inputs": [{ "name": "blockHeaderBytes", "type": "bytes" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "verifyTx(int256,int256,int256[],int256)",
    "type": "function",
    "inputs": [{ "name": "txHash", "type": "int256" }, { "name": "txIndex", "type": "int256" }, { "name": "sibling", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
=======
window.btcRelayAbi = [{"constant": false, "type": "function", "name": "cashOut(int256)", "outputs": [], "inputs": [{"type": "int256", "name": "numToken"}]}, {"constant": false, "type": "function", "name": "computeMerkle(int256,int256,int256[])", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "txHash"}, {"type": "int256", "name": "txIndex"}, {"type": "int256[]", "name": "sibling"}]}, {"constant": false, "type": "function", "name": "fastGetBlockHash(int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "blockHeight"}]}, {"constant": false, "type": "function", "name": "getAverageBlockDifficulty()", "outputs": [{"type": "int256", "name": "out"}], "inputs": []}, {"constant": false, "type": "function", "name": "getBlockHash(int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "blockHeight"}]}, {"constant": false, "type": "function", "name": "getBlockchainHead()", "outputs": [{"type": "int256", "name": "out"}], "inputs": []}, {"constant": false, "type": "function", "name": "getCumulativeDifficulty()", "outputs": [{"type": "int256", "name": "out"}], "inputs": []}, {"constant": false, "type": "function", "name": "getFeeVerifyTx()", "outputs": [{"type": "int256", "name": "out"}], "inputs": []}, {"constant": false, "type": "function", "name": "getLastBlockHeight()", "outputs": [{"type": "int256", "name": "out"}], "inputs": []}, {"constant": false, "type": "function", "name": "getTokenContract()", "outputs": [{"type": "int256", "name": "out"}], "inputs": []}, {"constant": false, "type": "function", "name": "inMainChain(int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "txBlockHash"}]}, {"constant": false, "type": "function", "name": "initTokenContract(int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "tokenFactoryAddr"}]}, {"constant": false, "type": "function", "name": "relayTx(bytes,uint256,int256,int256[],int256,int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "bytes", "name": "txStr"}, {"type": "uint256", "name": "txHash"}, {"type": "int256", "name": "txIndex"}, {"type": "int256[]", "name": "sibling"}, {"type": "int256", "name": "txBlockHash"}, {"type": "int256", "name": "contract"}]}, {"constant": false, "type": "function", "name": "setInitialParent(int256,int256,int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "blockHash"}, {"type": "int256", "name": "height"}, {"type": "int256", "name": "cumulativeDifficulty"}]}, {"constant": false, "type": "function", "name": "storeBlockHeader(bytes)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "bytes", "name": "blockHeaderBytes"}]}, {"constant": false, "type": "function", "name": "verifyTx(int256,int256,int256[],int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "txHash"}, {"type": "int256", "name": "txIndex"}, {"type": "int256[]", "name": "sibling"}, {"type": "int256", "name": "txBlockHash"}]}, {"constant": false, "type": "function", "name": "within6Confirms(int256)", "outputs": [{"type": "int256", "name": "out"}], "inputs": [{"type": "int256", "name": "txBlockHash"}]}, {"inputs": [], "type": "event", "name": "EthPayment()"}, {"inputs": [{"indexed": true, "type": "int256", "name": "errCode"}], "type": "event", "name": "Failure(int256)"}, {"inputs": [{"indexed": true, "type": "int256", "name": "blockHeight"}, {"indexed": false, "type": "address", "name": "rewardAddr"}], "type": "event", "name": "RewardToken(int256,address)"}]
>>>>>>> processTransaction in Solidity needs to match btcrelay so use uint256
