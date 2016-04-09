var ownerArr = ["0x9fc6fefd7f33ca29ee17f2bfec944695e5f29caf",
"0x235c751c615945c026855a6cbdeda8ea0db65cb7",
"0xfb365748c912fca6808db267342846645f3289e4",
"0xd005c515db902b1b77beb98370ba1f16b3111d7b"];  // hot account

var required = 2;
var dayLimit = web3.toWei(2, 'ether');

Wallet.new(ownerArr, required, dayLimit).then(function(instance) {
  // your contract is now deployed at instance.address
  console.log('@@@@ ', instance.address);

  // process.exit() call an unfortunate necessity
  process.exit();
});
