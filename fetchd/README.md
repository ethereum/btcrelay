### Why be a relayer for BTC Relay?

Everytime that a transaction is verified that's in a block header that you submit, you will earn Ether fees.  See [BTC Relay Incentives for Relayers](https://github.com/ethereum/btcrelay/tree/master#incentives-for-relayers)

### Quick Start

1. `pip install -r requirements.txt`

1. Run an Ethereum client, unlock an account with some Ether, and enable RPC (localhost and port 8545).

1. Get the [address of the BTC Relay contract](https://github.com/ethereum/btcrelay/tree/master#btc-relay-contract-address-and-abi)

1. `python fetchd.py -s <YourUnlockedAccount> -r <BTCRelayAddress> -n btc --rpcPort 8545 --fetch -d --gasPrice 200000000000`  use YourUnlockedAccount

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

## License

See [full MIT License](LICENSE) including:
```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
