window.btcToEthAbi = [{
    "name": "__getMetaForOutput(int256)",
    "type": "function",
    "inputs": [{ "name": "outNum", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256[]" }]
},
{
    "name": "__setupForParsing(string)",
    "type": "function",
    "inputs": [{ "name": "hexStr", "type": "string" }],
    "outputs": []
},
{
    "name": "doCheckOutputScript(string,int256,int256,int256)",
    "type": "function",
    "inputs": [{ "name": "rawTx", "type": "string" }, { "name": "size", "type": "int256" }, { "name": "outNum", "type": "int256" }, { "name": "expHashOfOutputScript", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "parseTransaction(string,int256,int256)",
    "type": "function",
    "inputs": [{ "name": "rawTx", "type": "string" }, { "name": "size", "type": "int256" }, { "name": "outNum", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256[]" }]
},
{
    "name": "processTransfer(string)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "string" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "readSimple(int256)",
    "type": "function",
    "inputs": [{ "name": "len", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "string" }]
},
{
    "name": "readUnsignedBitsLE(int256)",
    "type": "function",
    "inputs": [{ "name": "bits", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "readVarintNum()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "txinParse()",
    "type": "function",
    "inputs": [],
    "outputs": []
},
{
    "name": "txoutParse()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256[]" }]
}]
