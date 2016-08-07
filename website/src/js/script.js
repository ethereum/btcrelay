function getMainStatus() {
	if (typeof web3 !== 'undefined') {
    // Web3 has been injected by the browser (Mist/MetaMask)
    web3 = new Web3(web3.currentProvider);
  } else {
    // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
    web3 = new Web3(new Web3.providers.HttpProvider("http://frontier-lb.ether.camp"));
  }

  var heightPerRelay;

  $(function() {
    /*
      do NOT forget to update ABI files when needed
     */

     var relayAddr = '0x41f274c0023f83391de4e0733c609df5a124c3d4'; // Alpha Frontier

    // var relayAddr = web3.eth.namereg.addr('btcrelay');  // Olympic
    $('#relayAddr').text(relayAddr);


    updateBCI();
    updateBlockr();

    var RelayContract = web3.eth.contract(btcRelayAbi);  // see ./js/btcRelayAbi.js
    var contract = RelayContract.at(relayAddr);

    heightPerRelay = contract.getLastBlockHeight.call().toString();
    $('#latestBlockHeight').text(heightPerRelay);

    var headHash = contract.getBlockchainHead.call();
    $('#latestBlockHash').text(formatHash(headHash));

    var feeVTX = web3.fromWei(contract.getFeeAmount.call(headHash), 'ether');
    $('#feeVTX').text(feeVTX);

    var feeRecipient = contract.getFeeRecipient.call(headHash).toString(16);
    $('#feeRecipient').text('0x' + formatETHAddress(feeRecipient));

    window.btcrelayTester = contract;
    // signature of verifyTx is (txHash, txIndex, merkleSiblingArray, txBlockHash)
    // to make a call to verifyTx so that btcrelay will get some fees,
    // run this code in the browser developer console: fees will be sent
    // from the coinbase
    // res = btcrelayTester.verifyTx.sendTransaction(0, 1, [], 0, {from: web3.eth.coinbase, value: web3.toWei('0.1', 'ether')});
    // console.log('txHash for verifyTx: ', res)


    //setTimeout(checkHeights, 1000);
  });

  function updateBCI() {
    // 2 calls needed since https://blockchain.info/latestblock is missing CORS
    $.getJSON('https://blockchain.info/q/getblockcount?cors=true', function(data) {
      $('#bciBlockHeight').text(data);
    });

    // https://github.com/blockchain/api-v1-client-python/issues/17
    // $.getJSON('https://blockchain.info/q/latesthash?cors=true', function(data) {
    //   $('#bciBlockHash').text(data);
    // });
  }

  function updateBlockr() {
    $.getJSON('http://btc.blockr.io/api/v1/block/info/last', function(data) {
      $('#blockrBlockHeight').text(data.data.nb);
    });
  }

  function checkHeights() {
    var bciHeight = $('#bciBlockHeight').text();
    var blockrHeight = $('#blockrBlockHeight').text();
    if (!bciHeight || !blockrHeight ||
      heightPerRelay === bciHeight || heightPerRelay === blockrHeight) {
        $('#warnSync').hide();
    }
    else {
      $('#nodeBlockNum').text(web3.eth.blockNumber);
      $('#warnSync').show();
    }
  }

  function formatHash(bnHash) {
    var hash = bnHash.toString(16);
    return Array(64 - hash.length + 1).join('0') + hash;
  }

  function formatETHAddress(bnEthAddress) {
    var ethAddress = bnEthAddress.toString(16);
    return Array(40 - ethAddress.length + 1).join('0') + ethAddress;
  }
}

getMainStatus();