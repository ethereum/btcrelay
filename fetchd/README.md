### Quick Start

1. `pip install -r requirements.txt`

1. `python fetchd.py -s <YourUnlockedEthereumAccount> -r 0xb1d4c88a30a392aee6859e6f62738230db0c2d93 -n btc --rpcPort 8545 --fetch -d --gasPrice 500000000000`  use YourUnlockedEthereumAccount

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
