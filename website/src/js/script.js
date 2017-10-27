var web3;
var mainNetHost = 'https://mainnet.infura.io';
var testNetHost = 'https://morden.infura.io';
var mainNetAddr = '0x41f274c0023f83391de4e0733c609df5a124c3d4';
var testNetAddr = '0x5770345100a27b15f5b40bec86a701f888e8c601';
var mainNetStats = 'https://ethstats.net';
var testNetStats = 'https://morden.io';
var heightPerRelay;
var relayAddr;
var gMerkleProof;
var gBlockHashOfTx;
var gFeeVerifyEther;
var ContractClass;
var ContractObject;
var lastNet = null;
var isRelay = false;
var gProcessorAddr = '0x59c9fb53d658b15a7dded65c693703baf58cf63c'; // testnet Morden

var btcproof = require('bitcoin-proof');

/**
 *  Status Page
 */

function updatePage(net) {
  if (lastNet !== net) {
    lastNet = net;
    relayAddr = net === 'main' ? mainNetAddr : testNetAddr;

    if (typeof web3 !== 'undefined') {
      // Web3 has been injected by the browser (Mist/MetaMask)
      web3 = new Web3(web3.currentProvider);
    } else {
      web3 = new Web3(new Web3.providers.HttpProvider(net === 'main' ? mainNetHost : testNetHost));
    }

    $('#relayAddr').text(relayAddr);
    $('#relayAddr').attr('href', 'http://' + (net === 'test' ? 'testnet.' : '') + 'etherscan.io/address/' + relayAddr);

    $('#latestBlockHeight').text('# -');
    $('#bciBlockHeight').text('# -');
    $('#blockrBlockHeight').text('# -');
    $('#latestBlockHash').text('-');
    $('#feeRecipient').text('-');
    $('#feeRecipient').attr('href', '#');
    $('#feeVTX').text('-');
  }

  $('#warnSync').hide();

  setTimeout(function() {getStatus(net);}, 400);
}

function getStatus(net) {
  updateBCI();
  updateBlockr();

  ContractClass = web3.eth.contract(btcRelayAbi);
  ContractObject = ContractClass.at(relayAddr);

  ContractObject.getLastBlockHeight.call(function(err, heightPerRelay) {
    if (err) {
      console.log('@err getLastBlockHeight')
      return;
    }
    $('#latestBlockHeight').text('# ' + heightPerRelay);

    if (heightPerRelay.toNumber() === 0) {
      $('#warnSync').show();
    } else {
      $('#warnSync').hide();
    }
  });

  ContractObject.getBlockchainHead.call(function(err, headHash) {
    if (err) {
      console.log('@err getBlockchainHead')
      return;
    }
    $('#latestBlockHash').text(formatHash(headHash));

    ContractObject.getFeeAmount.call(headHash, function(err, feeWei) {
      if (err) {
        console.log('@@@ getFeeAmount error');
        return;
      }

      gFeeVerifyEther = web3.fromWei(feeWei, 'ether');
      $('#feeVTX').text(gFeeVerifyEther);
    });

    ContractObject.getFeeRecipient.call(headHash, function(err, feeRecipient) {
      if (err) {
        console.log('@@@ getFeeRecipient error');
        return;
      }
      $('#feeRecipient').text('0x' + formatETHAddress(feeRecipient));
      $('#feeRecipient').attr('href', 'http://' + (net === 'test' ? 'testnet.' : '') + 'etherscan.io/address/' + feeRecipient);
    })
  });

  window.btcrelayTester = ContractObject;
}

function updateBCI() {
  $.getJSON('https://blockchain.info/q/getblockcount?cors=true', function(data) {
    $('#bciBlockHeight').text('# ' + data);
  });
}

function updateBlockr() {
  $.getJSON('http://btc.blockr.io/api/v1/block/info/last', function(data) {
    $('#blockrBlockHeight').text('# ' + data.data.nb);
  });
}

function formatHash(bnHash) {
  var hash = bnHash.toString(16);
  return Array(64 - hash.length + 1).join('0') + hash;
}

function formatETHAddress(bnEthAddress) {
  var ethAddress = bnEthAddress.toString(16);
  return Array(40 - ethAddress.length + 1).join('0') + ethAddress;
}


/**
 *  Verify page
 */

// shows how to use web3 to make an eth_call to the relay contract
// verifyTx returns 1 (success) or 0 (verify failed)
function callVerifyTx(txBytes, txIndex, merkleSibling, txBlockHash) {
  // gFeeVerifyEther is transferred!  coinbase must have it or verifyTx fails
  var feeWei = web3.toWei(gFeeVerifyEther, 'ether');
  // var objParam = { from: web3.eth.coinbase, value: feeWei, gas: 3000000 };
  var objParam = { from: '0x102e61f5d8f9bc71d0ad4a084df4e65e05ce0e1c', value: feeWei, gas: 3000000 };
  var res = ContractObject.verifyTx.call(txBytes, txIndex, merkleSibling, txBlockHash, objParam);

  $('#txReturned').text(res.toString(16));
  $('.status-box .glyphicon').removeClass('glyphicon-repeat').removeClass('glyphicon-ok').removeClass('glyphicon-remove').removeClass('spinning');

  if(res.toString(16) === $('#btcTxHash').val()) {
    $('.status-box').addClass('success');
    $('.status-box .glyphicon').addClass('glyphicon-ok');
  } else {
    $('.status-box').addClass('danger');
    $('.status-box .glyphicon').addClass('glyphicon-remove');
  }
}

function callContract() {
  $('.status-box').removeClass('danger').removeClass('success');
  $('.status-box .glyphicon').removeClass('glyphicon-repeat').removeClass('glyphicon-ok').removeClass('glyphicon-remove').removeClass('spinning').addClass('glyphicon-repeat').addClass('spinning');
  var txBytes = '0x' + $('#rawTransaction').text();
  var txBlockHash = '0x' + gBlockHashOfTx;

  var merkleSibling = gMerkleProof.sibling.map(function(sib) {
    return '0x' + sib;
  });

  callVerifyTx(txBytes, gMerkleProof.txIndex, merkleSibling, txBlockHash);
}

function getTxInfo(isRelay) {
  if (typeof isRelay === 'undefined') {
    isRelay = false;
  }

  $('#rawTransaction').html('-');
  $('#merkleProof').html('-');
  $('#txBlockHash').html('-');
  $('#feeVerifyTx').html('-');
  $('#txReturned').html('-');
  $('.status-box').removeClass('danger').removeClass('success');
  $('.status-box .glyphicon').removeClass('glyphicon-repeat').removeClass('glyphicon-ok').removeClass('glyphicon-remove').removeClass('spinning').addClass('glyphicon-repeat');

  var txid = $('#btcTxHash').val();
  var urlJsonTx = "https://btc.blockr.io/api/v1/tx/raw/" + txid;
  $.getJSON(urlJsonTx, function(data) {
      $('#rawTransaction').text(data.data.tx.hex);

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
          $('#merkleProof').text(JSON.stringify(gMerkleProof));

          ContractObject.getFeeAmount.call('0x'+gBlockHashOfTx, function(err, feeWei) {
            if (err) {
              console.log('@@@ getFeeAmount error');
              return;
            }

            gFeeVerifyEther = web3.fromWei(feeWei, 'ether');
            $('#feeVerifyTx').text(gFeeVerifyEther);
          });
      })
  })
}

function doRelayTx(txBytes, txIndex, merkleSibling, txBlockHash) {
  // gFeeVerifyEther is transferred!  coinbase must have it or relayTx fails
  var feeWei = web3.toWei(gFeeVerifyEther, 'ether');
  var objParam = { from: web3.eth.coinbase, value: feeWei, gas: 1900000 };

  ContractObject.relayTx.sendTransaction(txBytes, txIndex, merkleSibling,
      txBlockHash, gProcessorAddr, objParam, function(err, ethTx) {
    if (err) {
      console.log('@@@ relayTx error');
      console.error(err);
      $('#txHashReturned').hide();
      $('#txHashError').show();
      $('.status-box').removeClass('danger').removeClass('success').addClass('danger');
      $('.status-box .glyphicon').removeClass('glyphicon-repeat').removeClass('glyphicon-ok').removeClass('glyphicon-remove').removeClass('spinning').addClass('glyphicon-remove');
      $('#txHashError').text(err.toString());
      return;
    }

    $('#txHashReturned').show();
    $('#txHashError').hide();
    $('.status-box').removeClass('danger').removeClass('success').addClass('success');
    $('.status-box .glyphicon').removeClass('glyphicon-repeat').removeClass('glyphicon-ok').removeClass('glyphicon-remove').removeClass('spinning').addClass('glyphicon-ok');
    $('#txHashReturned').text(ethTx);
    $('#txHashReturned').attr('href', 'http://' + (lastNet === 'test' ? 'testnet.' : '') + 'etherscan.io/tx/' + ethTx);
  });
}

function callRelayContract() {
  $('#txHashError').text('');
  $('#txHashError').hide();
  $('.status-box').removeClass('danger').removeClass('success');
  $('.status-box .glyphicon').removeClass('glyphicon-repeat').removeClass('glyphicon-ok').removeClass('glyphicon-remove').removeClass('spinning').addClass('glyphicon-repeat').addClass('spinning');
  var txBytes = '0x' + $('#rawTransaction').text();
  var txBlockHash = '0x' + gBlockHashOfTx;

  // web3.js wants 0x prepended
  var merkleSibling = gMerkleProof.sibling.map(function(sib) {
    return '0x' + sib;
  });

  doRelayTx(txBytes, gMerkleProof.txIndex, merkleSibling, txBlockHash);
}


/**
 *  Bindings
 */

$(function() {
  $('#btn-get-tx').click(getTxInfo);

  $('#btn-verify-tx').click(callContract);

  $('#btn-relay-tx').click(callRelayContract);
});
