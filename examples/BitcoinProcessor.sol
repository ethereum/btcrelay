/*
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

See the LICENSE file in https://github.com/ethereum/btcrelay for further details.

Example contract that can process Bitcoin transactions relayed to it via
BTC Relay.  This stores the Bitcoin transaction hash and the Ethereum block
number (so people running the same example with the same Bitcoin transaction
can get an indication that the storage was indeed updated).
*/
contract BitcoinProcessor {
    uint256 public lastTxHash;
    uint256 public ethBlock;

    address private _trustedBTCRelay;

    function BitcoinProcessor(address trustedBTCRelay) {
        _trustedBTCRelay = trustedBTCRelay;
    }

    // processTransaction should avoid returning the same
    // value as ERR_RELAY_VERIFY (in constants.se) to avoid confusing callers
    //
    // this exact function signature is required as it has to match
    // the signature specified in BTCRelay (otherwise BTCRelay will not call it)
    function processTransaction(bytes txn, uint256 txHash) returns (int256) {
        log0("processTransaction called");

        // only allow trustedBTCRelay, otherwise anyone can provide a fake txn
        if (msg.sender == _trustedBTCRelay) {
            log1("processTransaction txHash, ", bytes32(txHash));
            ethBlock = block.number;
            lastTxHash = txHash;
            // parse & do whatever with txn
            // For example, you should probably check if txHash has already
            // been processed, to prevent replay attacks.
            return 1;
        }

        log0("processTransaction failed");
        return 0;
    }
}
