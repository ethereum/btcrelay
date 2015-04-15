window.btcRelayAbi = [{
    "name": "computeMerkle(int256,int256,int256[],int256[])",
    "type": "function",
    "inputs": [{ "name": "tx", "type": "int256" }, { "name": "proofLen", "type": "int256" }, { "name": "hash", "type": "int256[]" }, { "name": "path", "type": "int256[]" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "fastHashBlock(string)",
    "type": "function",
    "inputs": [{ "name": "blockHeaderBinary", "type": "bytes" }],
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
    "name": "inMainChain(int256)",
    "type": "function",
    "inputs": [{ "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "init333k()",
    "type": "function",
    "inputs": [],
    "outputs": []
},
{
    "name": "logAnc(int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }],
    "outputs": []
},
{
    "name": "relayTx(string,int256,int256,int256[],int256[],int256,int256)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "bytes" }, { "name": "txHash", "type": "int256" }, { "name": "proofLen", "type": "int256" }, { "name": "hash", "type": "int256[]" }, { "name": "path", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }, { "name": "contract", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "saveAncestors(int256,int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }, { "name": "hashPrevBlock", "type": "int256" }],
    "outputs": []
},
{
    "name": "storeBlockHeader(string)",
    "type": "function",
    "inputs": [{ "name": "blockHeaderBinary", "type": "bytes" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "setPreGenesis(int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }],
    "outputs": []
},
{
    "name": "testingonlySetHeaviest(int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }],
    "outputs": []
},
{
    "name": "verifyTx(int256,int256,int256[],int256[],int256)",
    "type": "function",
    "inputs": [{ "name": "tx", "type": "int256" }, { "name": "proofLen", "type": "int256" }, { "name": "hash", "type": "int256[]" }, { "name": "path", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "within6Confirms(int256)",
    "type": "function",
    "inputs": [{ "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
