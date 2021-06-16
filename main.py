from gooey import Gooey, GooeyParser
import json
import hashlib

@Gooey(program_name='Asset registry contract calculator')
def main():
    parser = GooeyParser(description='Create a valid contract for Blockstream asset registry.')
    parser.add_argument('name', metavar='Name', help='Asset name', gooey_options={'validator':{'test': 'len(user_input) > 2', 'message': 'Min 3 chars'}})
    parser.add_argument('ticker', metavar='Ticker', help='Asset ticker', gooey_options={'validator':{'test': ' 1 < len(user_input) < 6', 'message': 'Max 5 chars'}})
    parser.add_argument('precision', help='Asset precision (0-8)', widget='IntegerField', gooey_options={'validator':{'test': '-1 < user_input < 9', 'message': 'Need a valid pubkey'}, 'min': 0, 'max': 8})
    parser.add_argument('domain', metavar='Domain', help='Asset domain', gooey_options={'validator':{'test': 'len(user_input) > 4', 'message': 'Need a valid website'}})
    parser.add_argument('pubkey', metavar='PubKey', help='Public Key', gooey_options={'validator':{'test': 'len(user_input) > 10', 'message': 'Need a valid pubkey'}})
    args = parser.parse_args()
    contract_obj = {'name':args.name, 'ticker':args.ticker, 'precision':int(args.precision), 'entity':{'domain':args.domain}, 'issuer_pubkey':args.pubkey, 'nonce': '47', 'version':0}
    contract = json.dumps(contract_obj, separators=(',',':'), sort_keys=True)
    sha256_c = hashlib.sha256()
    sha256_c.update(contract.encode('ascii'))
    contract_hash = sha256_c.hexdigest()
    contract_hash_rev = bytes.fromhex((contract_hash))[::-1].hex()
    print('Formatted contract')
    print(contract)
    print()
    print('Contract hash')
    print(contract_hash_rev)
    print()
    print('Now you can issue your asset with command:')
    print(f'elements-cli issuasset 1000 1 false {contract_hash_rev}')

if __name__ == '__main__':
    main()
