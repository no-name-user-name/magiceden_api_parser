from pprint import pprint

from magiceden_api import MagicParser
#  setup parser
mp = MagicParser(profile='example', driver_headless=True)

#  get most popular collection per 5 min.
collection = mp.get_popular_collections(limit=1, period='5m')[0]
# pprint(collection)

# symbol - its like collection name
symbol = collection['collectionSymbol']
name = collection['name']

# get all holders our most popular "collection"
holders = mp.get_holders(collection_symbol=symbol)['topHolders']
# pprint(holders)

for holder in holders:
    wallet = holder['owner']
    have_tokens = holder['tokens']
    spend_money = holder['buy7d']['volume'] / 10 ** 9

    # let's see who these guys are
    user = mp.get_user_info(holder_wallet=wallet)

    # filter
    if user == {} or 'displayName' not in user or 'username' not in user:
        continue

    data = f"""
- Wallet {user['walletAddress']}
- Display Name: {user["displayName"]}
- Username: @{user["username"]}
- Telegram: {user['telegram']}
------------------------------
- Have collection "{collection['name']}"
- Tokens count: {have_tokens}
- Spend money: {spend_money} SOL
"""
    print(data)

""" Result:

- Wallet 7eZ13PLeAs4geXt4RZs8YX4W1H8bW8dTgd1M3gF6H2zu
- Display Name: Austin Guo
- Username: @austinguooo
- Telegram: {}
------------------------------
- Have collection "ABC"
- Tokens count: 51
- Spend money: 399.0627148 SOL

"""