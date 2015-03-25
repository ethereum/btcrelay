

var padLeft = function (string, chars) {
    return new Array(chars - string.length + 1).join("0") + string;
};

function testCall() {
  console.log('@@@ in testCall')
  var bethAddress = '0x3432c7f5ca6552fca2f641575135578cb724eb1f';
  var contract = web3.eth.contract(bethAddress, btcRelayAbi);

  var block100K = '0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710'
  var words = CryptoJS.enc.Hex.parse(block100K);
  var blockBinaryStr = CryptoJS.enc.Latin1.stringify(words);

  var res = contract.call().fastHashBlock(blockBinaryStr);
  console.log('@@@@ res: ', res)
  document.getElementById('result').innerText = res.toString(10);
}


function testDirectprocessTransaction() {
  console.log('@@@ in testDirectprocessTransaction')
  console.log('@@@ btcToEthAbi: ', btcToEthAbi)

  var addrExchContract = '0x1ddb229746359a5eb72317f9936411be1b589301';
  var exch = web3.eth.contract(addrExchContract, btcToEthAbi);

  var txHex = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000';
  var res = exch.call().processTransaction(txHex);
  console.log('@@@@ res: ', res)
  document.getElementById('result').innerText = res.toString(10);
}


function testSampleCallingprocessTransaction() {
  console.log('@@@ in callContract')

  var addr = '0xc0b70bcf0c0b60ba5e15de1f8980ae357196a34a';
  var abi =
  [{
    "name": "callsA(string,int256)",
    "type": "function",
    "inputs": [{ "name": "txHex", "type": "string" }, { "name": "x", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
  }];

  var conA = '0x1ddb229746359a5eb72317f9936411be1b589301';
  var txHex = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000';
  var ct = web3.eth.contract(addr, abi);
  var res = ct.call().callsA(txHex, new BigNumber(conA));
  console.log('@@@@ res: ', res)
  document.getElementById('result').innerText = res.toString(10);
}


function testEthTransfer() {
  console.log('@@@ in testEthTransfer')
  console.log('@@@ btcRelayAbi: ', btcRelayAbi)

  var bethAddress = '0x3432c7f5ca6552fca2f641575135578cb724eb1f';
  var contract = web3.eth.contract(bethAddress, btcRelayAbi);

  var txHash = new BigNumber('0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4');
  var merkleSibling = [new BigNumber('0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87'),
    new BigNumber('0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49')];
  var merklePath = [1, 2];
  var proofLen = merkleSibling.length;
  // var merklePath = [new BigNumber(1), new BigNumber(2)];
  // var proofLen = new BigNumber(merkleSibling.length);
  var txBlockHash = new BigNumber('0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506');



  // var res = contract.call().verifyTx(txHash, proofLen, merkleSibling, merklePath, txBlockHash);
  // console.log('@@@@ res: ', res)
  // document.getElementById('result').innerText = res.toString(10);


  var txHex = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000';
  // var words = CryptoJS.enc.Hex.parse(txHex);
  // var txBinaryStr = CryptoJS.enc.Latin1.stringify(words);

  var exchangeContractAddr = new BigNumber('0x1ddb229746359a5eb72317f9936411be1b589301');
  var res = contract.call().relayTx(txHex, txHash, proofLen, merkleSibling, merklePath, txBlockHash, exchangeContractAddr);
  console.log('@@@@ res: ', res)
  document.getElementById('result').innerText = res.toString(10);








  // param = 9;
  // var param = parseInt(document.getElementById('value').value);
  //
  // var res = contract.call().processTransaction(param);
  // // var res = contract.transact().processTransaction('1300');
  // document.getElementById('result').innerText = res.toString(10);


  // 34 chars
  // contract.btest('1234567890123456789012345678901234').transact().then(function(res) {
  //         document.getElementById('result').innerText = res[0];
  //     });

  // contract.callsA(['0x77'], '0x205215f022af4950618730bcfae161b28397bc41').transact().then(function(res) {
  //           document.getElementById('result').innerText = res[0];
  //       });

        // this should be generated by ethereum
        //var param = parseInt(document.getElementById('value').value);
        // call the contract
        // var extra = {};
        // extra.to =
        // // extra.data = ''
        // //extra.data = param;
        // extra.data = "0x" + padLeft((11).toString(16), 64);
        // web3.eth.transact(extra).then(function(res) {
        //     document.getElementById('result').innerText = res[0];
        // });
        //
        //
  // var extra = {};
  // extra.to = bethAddress;
  // extra.data = '0x000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000b000000000000000000000000205215f022af4950618730bcfae161b28397bc41'
  // web3.eth.transact(extra).then(function(res) {
  //     document.getElementById('result').innerText = res[0];
  // });
}
