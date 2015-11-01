### Quick Start

1. `pip install -r requirements.txt`

1. Run Geth connected to the public testnet: https://github.com/ConsenSys/ConsenSys.github.io/wiki/ConsenSys-public-testnet  Use its faucet to get testnet ether, unlock an account, and enable RPC.

1. Get BTCRelayAddress from: http://cdn.rawgit.com/ethereum/btcrelay/master/examples/relayContractStatus.html

1. `python fetchd.py -s <YourUnlockedAccount> -r <BTCRelayAddress> -n btc --rpcPort 8545 --fetch -d --gasPrice 500000000000`  use YourUnlockedAccount

If you want to set a fee, which is specified in units of wei, add `--fee <weiAmount>`

The `-d` runs in daemon mode, so remove it if undesired.


### Recommended

Before `pip install -r requirements.txt` you may want to use a virtualenv and
may need to do the following:

1. `sudo apt-get install python-pip python-dev libssl-dev`
1. `pip install virtualenv`

Then these steps:
```
$ cd my_project_folder
$ virtualenv venv
$ source venv/bin/activate
```
http://docs.python-guide.org/en/latest/dev/virtualenvs/
