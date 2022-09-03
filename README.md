MagicEden API parser based on [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver).

You can parse all data regardless of Cloudflare.

```python
from magiceden_api import MagicParser

#  setup parser
mp = MagicParser(profile='example', driver_headless=True)

#  get most popular collection per 5 min.
collection = mp.get_popular_collections(limit=1, period='5m')[0]

# symbol - its like collection name
symbol = collection['collectionSymbol']
name = collection['name']

# get all holders our most popular "collection"
holders = mp.get_holders(collection_symbol=symbol)['topHolders']
```
[Full example](https://github.com/no-name-user-name/magiceden_api_parser/blob/master/examples/nft_holders_parser.py)


Some Methods:
- get_magiceden_volumes()
- get_all_collections()
- get_popular_collections()
- get_launchpad_collections()
- get_auctions()
- get_drops()
- get_most_watched_collections()
- get_twitter_followers()
- get_floor_price()
- get_holders()
- get_user_info()
- get_user_listings()
- get_user_activity()
- get_nfts_by_owner()
