window.btcRelayAbi = [{
    "name": "bulkStoreHeader(bytes,int256)",
    "type": "function",
    "inputs": [{ "name": "headersBinary", "type": "bytes" }, { "name": "count", "type": "int256" }],
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
    "inputs": [{ "name": "blockHeaderBinary", "type": "bytes" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "verifyTx(int256,int256,int256[],int256)",
    "type": "function",
    "inputs": [{ "name": "txHash", "type": "int256" }, { "name": "txIndex", "type": "int256" }, { "name": "sibling", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
