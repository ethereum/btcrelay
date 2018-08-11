import "./constants" as constants;
contract incentive is constants
{
    // # Incentive for block header relayers is they can set a fee for use of
    // # the header they store: they are the initial feeRecipient.
    // # By paying a changeRecipientFee to feeRecipient, anyone can lower the fee and
    // # become the feeRecipient: this is a mechanism to prevent excessive fees.
    // #
    // # Tested by test/test_fee.py

    // # first 16 bytes are the last gas price; last 16 bytes is the changeRecipientFee
    bytes32 gasPriceAndChangeRecipientFee;

    event EthPayment(address indexed recipient, uint256 amount);


    //# sets _feeInfo for the block and updates gasPriceAndChangeRecipientFee
    function storeBlockWithFee(bytes32 blockHeaderBytes, uint256 feeWei) returns(bool)
    {
        return this.storeBlockWithFeeAndRecipient(blockHeaderBytes, feeWei, msg.sender);
    }

    //# this indirection is needed by test_fee.py, but a configurable recipient may turn out useful
    function storeBlockWithFeeAndRecipient(bytes32 blockHeaderBytes, uint256 feeWei, address feeRecipient) returns(bool)
    {
        uint256 beginGas = msg.gas;
        bool res = this.storeBlockHeader(blockHeaderBytes);
        if(res)
        {
            bytes32 blockHash = m_dblShaFlip(blockHeaderBytes);
            m_setFeeInfo(blockHash, feeWei, feeRecipient);
            uint256 remainingGas = msg.gas;
            // # currGP is tx.gasprice clamped within 1/1024 of gLastGasPrice
            // # (1/1024 is the same factor used for adjusting Ethereum's block gas limit)
            uint256 gLastGasPrice = m_getLastGasPrice();
            uint256 minGP = 1023 * gLastGasPrice / 1024;
            uint256 maxGP = 1025 * gLastGasPrice / 1024;
            if(tx.gasprice < minGP)
            {
                currGP = minGP;
            }
            else if(tx.gasprice > maxGP)
            {
                currGP = maxGP;
            }
            else
            {
                currGP = tx.gasprice;
            }
            uint gChangeRecipientFee = 2 * currGP * (beginGas - remainingGas);  //# 2X the cost of storing the header
            m_setGasPriceAndChangeRecipientFee(currGP, gChangeRecipientFee);
            return res;
        }
        return false;

    }

    // # if sufficient fee for 'txBlockHash' is provided, pay the feeRecipient
    // # and return 1.  otherwise return 0.
    // # It is the recipient's responsibility to accept the fee.
    // # This does NOT return any funds to incorrect callers
    function feePaid(bytes32 txBlockHash, uint256 amountWei) public payable returns(uint256)
    {
        if(msg.value >= amountWei)
        {
            if(msg.value > 0)
            {
                address feeRecipient = m_getFeeRecipient(txBlockHash);
                if(this.depthCheck(0))
                {
                    feeRecipient.transfer(msg.value);
                }
            }
            return 1;
        }
        return 0;
    }

    // # callers must sufficiently send the block's current fee, AND feeWei must be LESS
    // # than the block's current fee
    // # This does NOT return any funds to incorrect callers
    function changeFeeRecipient(bytes32 blockHash, uint256 feeWei, address feeRecipient) public payable returns(uint256)
    {
        if(this.feePaid(blockHash, m_getChangeRecipientFee(), msg.value))
        {
            return 0;
        }
        //# feeWei is only allowed to decrease
        if(feeWei < m_getFeeAmount(blockHash))
        {
            m_setFeeInfo(blockHash, feeWei, feeRecipient);
            return 1;
        }

        return 0;
    }

    function getFeeRecipient(bytes32 blockHash) returns(address)
    {
        return m_getFeeRecipient(blockHash);
    }

    function getFeeAmount(bytes32 blockHash) returns(uint256)
    {
        return m_getFeeAmount(blockHash);
    }

    function getChangeRecipientFee() returns(uint256)
    {
        return m_getChangeRecipientFee();
    }

    // # since calling depthCheck itself is a CALL, this function
    // # depthCheck returns 1 if n+1 CALL depth is available.
    // # Thus calling depthCheck(0) will return 1 if a CALL is available: ie CALL
    // # depth is at most 1023.
    // #
    // # Important note if porting/using this in Solidity, and make sure to test
    // # boundary conditions CALL depth carefully -- from Martin Swende:
    // # In Solidity, all internal "calls" are implemented using JUMP:s, since
    // # CALL is at least 5 times as expensive. And JUMP does not increase the
    // # CALL stack.
    // #
    // # So in order to do depth-check in Solidity, this won't work:
    // # contract foo{
    // #         depth_check(n) return (uint){
    // #                 if (n > 0) return depth_check(n-1)
    // #                 else return 1;
    // #         }
    // # }
    // #
    // # Instead, a level of explicit casting is required to trick Solidity to use
    // # call, like this:
    // #
    // # contract foo{
    // #         depth_check(n) return(uint){
    // #                 if (n > 0) return foo(self).depth_check(n-1)
    // #                 else return 1;
    // #         }
    // # }

    function depthCheck(uint256 n)
    {
        if(n != 0) {
            return this.depthCheck(n - 1);
        }
        return 1;
    }

    // #
    // # macros for a block's _feeInfo
    // #
    // # _feeInfo has first 20 bytes as the feeRecipient and
    // # the last 12 bytes is the feeAmount
    // #
    function m_getFeeInfo(bytes32 blockHash) returns(bytes32)
    {
        return bitcoinBlock[blockHash]._feeInfo;
    }

    function m_setFeeInfo(bytes32 blockHash, uint256 feeWei, address feeRecipient)
    {
        if(feeWei > 0xffffffffffffffffffffffff)
        {
            feeWei = 0xffffffffffffffffffffffff;
        }
        bitcoinBlock[blockHash]._feeInfo = feeRecipient * BYTES_12 | feeWei;
    }

    function m_getFeeRecipient(bytes32 blockHash)
    {
        return div(m_getFeeInfo(blockHash), BYTES_12);
    }

    function m_getFeeAmount(bytes32 blockHash) returns(uint256)
    {
        return 0x0000000000000000000000000000000000000000ffffffffffffffffffffffff & m_getFeeInfo($blockHash);
    }

    // #
    // # macros for gasPriceAndChangeRecipientFee
    // #
    function m_getLastGasPrice() {
        return div(this.gasPriceAndChangeRecipientFee, BYTES_16);
    }

    function m_getChangeRecipientFee()
    {
        (0x00000000000000000000000000000000ffffffffffffffffffffffffffffffff & self.gasPriceAndChangeRecipientFee);
    }

    function m_setGasPriceAndChangeRecipientFee(uint256 gasPrice, uint256 changeRecipientFee)
    {
        this.gasPriceAndChangeRecipientFee = (gasPrice * BYTES_16) | changeRecipientFee;
    }

}
