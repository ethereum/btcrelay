pragma solidity ^0.4.17;
contract constants
{
    // Constants
    // for verifying Bitcoin difficulty
    uint256 DIFFICULTY_ADJUSTMENT_INTERVAL = 2016;  // Bitcoin adjusts every 2 weeks
    uint256 TARGET_TIMESPAN = 14 * 24 * 60 * 60;  // 2 weeks
    uint256 TARGET_TIMESPAN_DIV_4 = TARGET_TIMESPAN / 4;
    uint256 TARGET_TIMESPAN_MUL_4 = TARGET_TIMESPAN * 4;
    uint256 UNROUNDED_MAX_TARGET = 2**224 - 1;  // different from (2**16-1)*2**208 http =//bitcoin.stackexchange.com/questions/13803/how-exactly-was-the-original-coefficient-for-difficulty-determined

    //
    // Error / failure codes
    //

    // error codes for storeBlockHeader
    uint256 ERR_DIFFICULTY =  10010;  // difficulty didn't match current difficulty
    uint256 ERR_RETARGET = 10020;  // difficulty didn't match retarget
    uint256 ERR_NO_PREV_BLOCK = 10030;
    uint256 ERR_BLOCK_ALREADY_EXISTS = 10040;
    uint256 ERR_PROOF_OF_WORK = 10090;

    // error codes for verifyTx
    uint256 ERR_BAD_FEE = 20010;
    uint256 ERR_CONFIRMATIONS = 20020;
    uint256 ERR_CHAIN = 20030;
    uint256 ERR_MERKLE_ROOT = 20040;
    uint256 ERR_TX_64BYTE = 20050;

    // error codes for relayTx
    uint256 ERR_RELAY_VERIFY = 30010;

    uint256 BYTES_1 = 2**8;
    uint256 BYTES_2 = 2**16;
    uint256 BYTES_3 = 2**24;
    uint256 BYTES_4 = 2**32;
    uint256 BYTES_5 = 2**40;
    uint256 BYTES_6 = 2**48;
    uint256 BYTES_7 = 2**56;
    uint256 BYTES_8 = 2**64;
    uint256 BYTES_9 = 2**72;
    uint256 BYTES_10 = 2**80;
    uint256 BYTES_11 = 2**88;
    uint256 BYTES_12 = 2**96;
    uint256 BYTES_13 = 2**104;
    uint256 BYTES_14 = 2**112;
    uint256 BYTES_15 = 2**120;
    uint256 BYTES_16 = 2**128;
    uint256 BYTES_17 = 2**136;
    uint256 BYTES_18 = 2**144;
    uint256 BYTES_19 = 2**152;
    uint256 BYTES_20 = 2**160;
    uint256 BYTES_21 = 2**168;
    uint256 BYTES_22 = 2**176;
    uint256 BYTES_23 = 2**184;
    uint256 BYTES_24 = 2**192;
    uint256 BYTES_25 = 2**200;
    uint256 BYTES_26 = 2**208;
    uint256 BYTES_27 = 2**216;
    uint256 BYTES_28 = 2**224;
    uint256 BYTES_29 = 2**232;
    uint256 BYTES_30 = 2**240;
    uint256 BYTES_31 = 2**248;
    uint256 BYTES_32 = 2**256;
}
