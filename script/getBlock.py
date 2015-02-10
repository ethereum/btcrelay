from __future__ import print_function

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user=TODO
rpc_password=TODO

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
#best_block_hash = rpc_connection.getbestblockhash()
#print(rpc_connection.getblock(best_block_hash))


#startB=3
#commands = [ [ "getblockhash", height] for height in range(startB) ]


chunk = 1000
startB = 325001
for i in range(15):
	print(startB)
	endB = startB + chunk
	commands = [ [ "getblockhash", height] for height in range(startB,endB) ]
	block_hashes = rpc_connection.batch_(commands)
	blocks = rpc_connection.batch_([ [ "getblock", h, False ] for h in block_hashes ])

	with open('bh'+str(startB)+'.txt', 'w') as f:
	  for h in blocks:
	    print(h[:160], file=f)

	startB += chunk
