window.btcRelayAbi = [{
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
    "name": "saveAncestors(int256,int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }, { "name": "hashPrevBlock", "type": "int256" }],
    "outputs": []
},
{
    "name": "setInitialParent(int256,int256,int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }, { "name": "height", "type": "int256" }, { "name": "cumulativeDifficulty", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "storeBlockHeader(bytes)",
    "type": "function",
    "inputs": [{ "name": "blockHeaderBinary", "type": "bytes" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "testingonlySetHeaviest(int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }],
    "outputs": []
},
{
    "name": "verifyTx(int256,int256,int256[],int256)",
    "type": "function",
    "inputs": [{ "name": "txHash", "type": "int256" }, { "name": "txIndex", "type": "int256" }, { "name": "sibling", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "within6Confirms(int256)",
    "type": "function",
    "inputs": [{ "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
