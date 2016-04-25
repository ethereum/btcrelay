function testnetSampleCall() {

var web3 = require('web3');
    web3.setProvider(new web3.providers.HttpProvider('http://morden.cloudapp.net:8545'));

var btcproof = require('bitcoin-proof');

// var gRelayAddr = web3.eth.namereg.addr('btcrelay');
var gRelayAddr = '0x5770345100a27b15f5b40bec86a701f888e8c601';  // Morden
var gMerkleProof;
var gBlockHashOfTx;
var gFeeVerifyFinney;

var RelayContractClass = web3.eth.contract(btcRelayAbi);  // see ./js/btcRelayAbi.js
var gRelayContract = RelayContractClass.at(gRelayAddr);


// shows how to use web3 to make an eth_call to the relay contract
// verifyTx returns 1 (success) or 0 (verify failed)
function callVerifyTx(txBytes, txIndex, merkleSibling, txBlockHash) {
  // gFeeVerifyFinney is transferred!  coinbase must have it or verifyTx fails
  var feeWei = web3.toWei(gFeeVerifyFinney, 'finney');
  var objParam = { from: web3.eth.coinbase, value: feeWei, gas: 3000000 };
  var res = gRelayContract.verifyTx.call(txBytes, txIndex, merkleSibling, txBlockHash, objParam);

  document.getElementById('result').innerText = res.toString(16);
}

function callContract() {
  var txBytes = '0x' + $('#txHexText').val();
  // console.log('txBytes: ' + txBytes)
  var txBlockHash = '0x' + gBlockHashOfTx;

  // web3.js wants 0x prepended
  var merkleSibling = gMerkleProof.sibling.map(function(sib) {
    return '0x' + sib;
  });

  callVerifyTx(txBytes, gMerkleProof.txIndex, merkleSibling, txBlockHash);
}

// includes sample of using the bitcoin-proof module
function getTxInfo() {
  var txid = $('#transHex').val();
  var urlJsonTx = "https://btc.blockr.io/api/v1/tx/raw/" + txid;
  $.getJSON(urlJsonTx, function(data) {
      $('#txHexText').val(data.data.tx.hex);

      var blockNum = data.data.tx.blockhash;
      var blockInfoUrl = "http://btc.blockr.io/api/v1/block/raw/"+blockNum;
      $.getJSON(blockInfoUrl, function(res) {
          gBlockHashOfTx = res.data.hash;
          $('#txBlockHash').text(gBlockHashOfTx)

          var txIndex;
          for (var key in res.data.tx) {
            if (res.data.tx[key] == txid) {
              txIndex = key;
              break;
            }
          }

          gMerkleProof = btcproof.getProof(res.data.tx, txIndex);
          console.log('merkle proof: ', gMerkleProof)
          $('#mProof').val(JSON.stringify(gMerkleProof));

          gFeeVerifyFinney = web3.fromWei(gRelayContract.getFeeAmount.call('0x'+gBlockHashOfTx), 'finney');
          $('#feeVerifyTx').text(gFeeVerifyFinney);
      })
  })
}


  console.log('in testnetSampleCall')
  // tx[1] of block 408000
  $('#transHex').val('dd059634699e85b51af4964ab97d5e75fb7cd86b748d0ee1c537ca1850101dc7');
  $('#btn-get-tx').click(getTxInfo);
  $('#relayAddr').text(gRelayAddr);

  return {
    callContract: callContract
  }
}
