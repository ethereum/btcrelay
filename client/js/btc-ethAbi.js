window.btcToEthAbi = [{
    "name": "getFirst2Outputs(string)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "bytes" }],
    "outputs": [{ "name": "out", "type": "int256[]" }]
},
{
    "name": "getUnsignedBitsLE(string,int256,int256)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "bytes" }, { "name": "pos", "type": "int256" }, { "name": "bits", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256[]" }]
},
{
    "name": "processTransaction(string,int256)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "bytes" }, { "name": "txHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "setOwner(int256)",
    "type": "function",
    "inputs": [{ "name": "newOwner", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "setTrustedBtcRelay(int256)",
    "type": "function",
    "inputs": [{ "name": "trustedRelayContract", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "testingonlySetBtcAddr(int256)",
    "type": "function",
    "inputs": [{ "name": "btcAddr", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
