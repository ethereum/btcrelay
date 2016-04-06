var addr = ["0x9fc6fefd7f33ca29ee17f2bfec944695e5f29caf",
"0x235c751c615945c026855a6cbdeda8ea0db65cb7",
"0xfb365748c912fca6808db267342846645f3289e4"];

var required = 2;
var dayLimit = 900;

Wallet.new(addr, required, dayLimit).then(function(instance) {
  console.log('@@@@ ', instance.address);
  // your contract is now deployed at instance.address
  
  // process.exit() call an unfortunate necessity
  process.exit();
});
