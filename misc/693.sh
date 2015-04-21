#!/bin/sh

# toAddr="0x57b723e224954a3026c1fb44c5f07b4b5fc096a8"

a=0

while [ $a -lt 2 ]
do
   echo $a
   curl -X POST --data '{"jsonrpc":"2.0","method":"eth_sendTransaction","params":[{
     "from": "0xcd2a3d9f938e13cd947ec05abc7fe734df8dd826",
     "to": "0x57b723e224954a3026c1fb44c5f07b4b5fc096a8",
     "gas": "0x76c0",
     "gasPrice": "0x9184e72a000",
     "value": "0x1"
   }
   ],"id":1}' http://localhost:8080

   curl -X POST --data '{"jsonrpc":"2.0","method":"eth_getTransactionCount","params":[
    "0xcd2a3d9f938e13cd947ec05abc7fe734df8dd826",
    "pending"
   ],"id":1}' http://localhost:8080

   a=`expr $a + 1`
done
