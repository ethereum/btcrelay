var web3;
var mainNetHost = 'http://frontier-lb.ether.camp';
var testNetHost = 'https://morden.infura.io:8545';
var mainNetAddr = '0x41f274c0023f83391de4e0733c609df5a124c3d4';
var testNetAddr = '0x5770345100a27b15f5b40bec86a701f888e8c601';
var heightPerRelay;
var relayAddr;
var gMerkleProof;
var gBlockHashOfTx;
var gFeeVerifyFinney;
var ContractClass;
var ContractObject;
var lastNet = null;

var btcproof = require('bitcoin-proof');

/**
 *  Status Page
 */

function updatePage(net) {
  if (lastNet !== net) {
    lastNet = net;
    relayAddr = net === 'main' ? mainNetAddr : testNetAddr;

    web3 = new Web3(new Web3.providers.HttpProvider(net === 'main' ? mainNetHost : testNetHost));

    $('#header').html((net === 'main' ? 'Main' : 'Test') + ' net live status' + (net === 'test' ? ' <small>(may need relayers)</small>' : ''));
    $('#relayAddr').text(relayAddr);
  }

  $('#warnSync').hide();

  setTimeout(function() {getStatus(net);}, 400);
}

function getStatus(net) {
  updateBCI();
  updateBlockr();

  ContractClass = web3.eth.contract(btcRelayAbi);
  ContractObject = ContractClass.at(relayAddr);

  heightPerRelay = ContractObject.getLastBlockHeight.call().toString();
  $('#latestBlockHeight').text(heightPerRelay);

  var headHash = ContractObject.getBlockchainHead.call();
  $('#latestBlockHash').text(formatHash(headHash));

  var feeVTX = web3.fromWei(ContractObject.getFeeAmount.call(headHash), 'ether');
  $('#feeVTX').text(feeVTX);

  var feeRecipient = ContractObject.getFeeRecipient.call(headHash).toString(16);
  $('#feeRecipient').text('0x' + formatETHAddress(feeRecipient));

  window.btcrelayTester = ContractObject;

  setTimeout(checkHeights, 1000);
}

function updateBCI() {
  $.getJSON('https://blockchain.info/q/getblockcount?cors=true', function(data) {
    $('#bciBlockHeight').text(data);
  });
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


/**
 *  Verify page
 */

// shows how to use web3 to make an eth_call to the relay contract
// verifyTx returns 1 (success) or 0 (verify failed)
function callVerifyTx(txBytes, txIndex, merkleSibling, txBlockHash) {
  // gFeeVerifyFinney is transferred!  coinbase must have it or verifyTx fails
  var feeWei = web3.toWei(gFeeVerifyFinney, 'finney');
  // var objParam = { from: web3.eth.coinbase, value: feeWei, gas: 3000000 };
  var objParam = { from: '0x102e61f5d8f9bc71d0ad4a084df4e65e05ce0e1c', value: feeWei, gas: 3000000 };
  var res = ContractObject.verifyTx.call(txBytes, txIndex, merkleSibling, txBlockHash, objParam);

  $('#txReturned').text(res.toString(16));
}

function callContract() {
  var txBytes = '0x' + $('#rawTransaction').text();
  var txBlockHash = '0x' + gBlockHashOfTx;

  var merkleSibling = gMerkleProof.sibling.map(function(sib) {
    return '0x' + sib;
  });

  callVerifyTx(txBytes, gMerkleProof.txIndex, merkleSibling, txBlockHash);
}

function getTxInfo() {
  $('#rawTransaction').html('-');
  $('#merkleProof').html('-');
  $('#txBlockHash').html('-');
  $('#feeVerifyTx').html('-');
  $('#txReturned').html('-');

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

          gFeeVerifyFinney = web3.fromWei(ContractObject.getFeeAmount.call('0x'+gBlockHashOfTx), 'finney');
          $('#feeVerifyTx').text(gFeeVerifyFinney);
      })
  })
}


/**
 *  Bindings
 */

$(function() {
  $('.example-page').hide();
  $('.example-list li').removeClass('active');

  $('#mainnetHeading').on('click', function(e) {
    $(this).find('li.header').removeClass('active').addClass('active');
    $('#testnetHeading').find('li.header').removeClass('active');
    $('.example-page').hide();
    $('.example-list li').removeClass('active');
    $('#statusPage').show();
    updatePage('main');
  });

  $('#testnetHeading').on('click', function(e) {
    $(this).find('li.header').removeClass('active').addClass('active');
    $('#mainnetHeading').find('li.header').removeClass('active');
    $('.example-page').hide();
    $('.example-list li').removeClass('active');
    $('#statusPage').show();
    updatePage('test');
  });

  updatePage('main');

  $('.verifyTxPage').on('click', function(e) {
    $('.example-page').hide();
    $('.example-list li').removeClass('active');
    $(this).parent().addClass('active');
    $('#statusPage').hide();


    // Reset fields
    $('#btcTxHash').val('dd059634699e85b51af4964ab97d5e75fb7cd86b748d0ee1c537ca1850101dc7');
    $('#rawTransaction').html('-');
    $('#merkleProof').html('-');
    $('#txBlockHash').html('-');
    $('#feeVerifyTx').html('-');
    $('#txReturned').html('-');
    $('#verifyPage').show();

    $('#header').html('Verify Tx <small>' + (lastNet === 'main' ? '(Main net)' : '(Morden test net)') + '</small>');
  });

  $('#btn-get-tx').click(getTxInfo);

  $('#btn-verify-tx').click(callContract);
});