from pyepm import api, config
import serpent

CONTRACT_FILE = "btcrelay.py"
CONTRACT_GAS = 56000

ETHER = 10 ** 18



api_config = config.read_config()
instance = api.Api(api_config)

contract = serpent.compile(open(CONTRACT_FILE).read()).encode('hex')
contract_address = instance.create(contract, gas=CONTRACT_GAS)
print "Contract will be available at %s" % contract_address
if True #args.wait:
    instance.wait_for_next_block(verbose=True)
print "Is contract?", instance.is_contract_at(contract_address)
