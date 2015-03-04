window.btcToEthAbi = [{
    "name": "getFirst2Outputs(string)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "string" }],
    "outputs": [{ "name": "unknown_out", "type": "int256[]" }]
},
{
    "name": "getUnsignedBitsLE(string,int256,int256)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "string" }, { "name": "pos", "type": "int256" }, { "name": "bits", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256[]" }]
},
{
    "name": "processTransfer(string)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "string" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
