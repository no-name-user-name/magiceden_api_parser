import os
import sys
import json
import time
import logging
from urllib.parse import quote, urlencode

import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

logger = logging.getLogger('MagicParser')

formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)
logger.setLevel(logging.ERROR)


class MagicParser:
    def __init__(self, profile: str = 'main', driver_headless: bool = True, temp_dir_path: str = None):
        """
        MagicEden api parser


        profile: Chrome profile name

        driver_headless: Chrome Headless mode

        temp_dir_path: Chrome profile dir
        """
        self.session = requests.Session()

        if temp_dir_path is None:
            temp_dir_path = f"{os.getcwd()}\\_temp\\profile_{profile}".replace('\\', '\\\\')

        os.makedirs(temp_dir_path, exist_ok=True)
        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.page_load_strategy = 'eager'
        options.headless = driver_headless
        self.driver = uc.Chrome(options=options, user_data_dir=temp_dir_path, use_subprocess=True)

    def _request(self, url, retry_timeout=5):
        r = None
        is_error = True
        while is_error:
            try:
                r = self.session.get(url, timeout=30)
                is_error = False
            except Exception as e:
                logger.debug(e)
                time.sleep(retry_timeout)

        if r.status_code == 200:
            return r.json()
        else:
            while True:
                try:
                    return self._driver_request(url)
                except Exception as e:
                    logger.debug(e)
                    time.sleep(retry_timeout)

    def _driver_request(self, url):
        self.driver.get(url)
        text = self.driver.find_element(By.TAG_NAME, 'body').get_attribute("textContent")
        return json.loads(text)

    def get_featured_carousels(self) -> list[dict]:
        """
        Get all data form Carousels on MagicEden main page

        :return: list of carousels data.
        """
        url = 'https://api-mainnet.magiceden.io/featured_carousels?edge_cache=true'
        return self._request(url)

    def get_featured_collections_carousels(self) -> list[dict]:
        """
        Get featured collections from MagicEden main page

        :return: list of featured collections.
        """
        url = 'https://api-mainnet.magiceden.io/featured_collections_carousels?edge_cache=true'
        return self._request(url)

    def get_magiceden_volumes(self) -> dict:
        """
        Get Total ME volumes and volumes per 24h

        :return: dict of volumes
        """
        url = 'https://api-mainnet.magiceden.io/volumes?edge_cache=true'
        return self._request(url)

    def get_all_collections(self) -> list[dict]:
        """
        Get all collections with little information

        :return: list of collections.
        """
        url = 'https://api-mainnet.magiceden.io/all_collections_with_escrow_data?edge_cache=true'
        return self._request(url)

    def get_all_organizations(self) -> list[dict]:
        """
        Get all organizations registered on ME and they bio

        :return: list of organizations.
        """
        url = 'https://api-mainnet.magiceden.io/all_organizations?edge_cache=true'
        return self._request(url)

    def get_popular_collections(self, limit=1000, period='1d') -> list[dict]:
        """
        Parse top collections per set period

        :param limit: items limit (1-1000)
        :param period: '5m', '15m', '1h', '6h', '1d', '7d', '30d'
        :return: list of collections.
        """

        if period not in ['5m', '15m', '1h', '6h', '1d', '7d', '30d']:
            print("Error! 'get_collections': period available states '5m', '15m', '1h', '6h', '1d', '7d', '30d'")
            exit()

        url = f"https://stats-mainnet.magiceden.io/collection_stats/popular_collections/sol?limit={limit}" \
              f"&window={period}"
        return self._request(url)

    def get_price(self, currency='SOL') -> dict:
        """
        Get price of SOL/ETH - USDC

        :param currency: 'SOL' / 'ETH'
        :return: dict with price data {symbol: "SOLUSDC", price: "31.64000000"}
        """
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={currency}USDC'
        return self._request(url)

    def get_launchpad_collections(self) -> list[dict]:
        """
        Get list of launchpad collections

        :return: list of launchpad collections
        """
        url = 'https://api-mainnet.magiceden.io/launchpad_collections?edge_cache=true'
        return self._request(url)

    def get_auctions(self, status='live', timeout=30000) -> list[dict]:
        """
        Get auctions list

        :param status: live | upcoming | finished
        :param timeout: period limit
        :return: list of auctions
        """
        sort = '%7B%22config.endDate%22:1%7D'
        if status == 'upcoming':
            sort = '%7B%22config.startDate%22:1%7D'

        elif status == 'finished':
            sort = '%7B%22config.endDate%22:-1%7D&limit=20&'

        url = f'https://api-mainnet.magiceden.io/auctions?status={status}&sort={sort}&' \
              f'edge_cache=true&timeout={timeout}'
        return self._request(url)

    def get_auction_by_symbol(self, collection_symbol):
        # search_params = {"$match": {}, "$sort": {"price": 1}, "$skip": 0, "$limit": 20} not now
        url = f'https://api-mainnet.magiceden.io/auctions/{collection_symbol}'
        return self._request(url)

    def get_drops(self, limit=500, offset=0, top=None) -> list[dict]:
        """
        Get Drops info. Top limit 10 or 15 collections

        :param offset: offset limit
        :param limit: [1-500] items limit
        :param top: 10 or 15 | Show top10 or top15
        :return: list of drops
        """

        params = {
            'limit': limit,
            'offset': offset
        }

        if top is not None:
            params['top'] = top

        url = f'https://api-mainnet.magiceden.io/drops?{urlencode(params)}'
        return self._request(url)

    def get_most_watched_collections(self) -> list[dict]:
        """
        Get list of collections most_watched

        :return: list of collections
        """
        url = 'https://api-mainnet.magiceden.io/collection_watchlists/most_watched?edge_cache=true'
        return self._request(url)

    def get_multi_collection_stats(self, collections_symbols: list) -> list[dict]:
        """

        :param collections_symbols:
        :return:
        """
        collections_symbols = ','.join(collections_symbols)
        url = f'https://api-mainnet.magiceden.io/rpc/getMultiCollectionEscrowStats/{collections_symbols}'
        return self._request(url)

    def get_collections_witch_symbols(self, collection_symbols: list) -> list[dict]:
        """
        Get collections by symbol

        :param collection_symbols: list of symbols ["degods","aurory"]
        :return: list collections info
        """

        collection_symbols = quote(str(collection_symbols)).replace('%27', '%22')
        url = f'https://api-mainnet.magiceden.io/rpc/getCollectionsWithSymbols?symbols={collection_symbols}'
        return self._request(url)

    def get_collection_escrow_stats(self, collection_symbol: str) -> dict:
        url = f'https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{collection_symbol}'
        return self._request(url)

    def get_collection(self, symbol: str) -> dict:
        """
        Get collection info

        {
            "symbol": "urbanites",
            "candyMachineIds": [
                "tMCL2JKBC8hFtEUdshUVsxCJU4BPv1ga5RM5RjBYNXt"
            ],
            "categories": [
                "pfps",
                null
            ],
            "createdAt": "2022-09-05T13:48:29.228Z",
            "description": "Generated and deployed on LaunchMyNFT.",
            "discord": "",
            "enabledAttributesFilters": true,
            "image": "https://nftstorage.link/ipfs/bafybeif2tczmvcms2hff7mxerboi6z6okvabml7vturpzwsa77a5cdidai/11.jpeg",
            "isAutolist": true,
            "lmnft": "https://www.launchmynft.io/collections/3wyrgBxtvEL43cqunsBqdTTeTNJn4uxnoqWDdHBTCEu7/MmQ43yEDD1AmyUDIgH4W",
            "name": "Urbanites",
            "rarity": {
                "showMoonrank": false,
                "showHowrare": true,
                "showMagicEden": true
            },
            "totalItems": 0,
            "twitter": "https://www.twitter.com/UrbanitesNft",
            "updatedAt": "2022-09-05T21:07:08.614Z",
            "watchlistCount": 5,
            "hasAllItems": true
        }

        :param symbol:
        :return:
        """
        url = f'https://api-mainnet.magiceden.io/collections/{symbol}'
        return self._request(url)

    def check_collection_scam_flag(self, collection_symbol: str) -> bool:
        """

        :param collection_symbol: symbol name of collection
        :return: False | True
        """

        url = f'https://api-mainnet.magiceden.io/collection_flags/check/{collection_symbol}'
        return self._request(url)['hasFlag']

    def get_twitter_followers(self, collection_symbol: str) -> int:
        """
        Get collection twitter followers count

        :param collection_symbol: collection symbol
        :return: int followers count
        """
        url = f'https://stats-mainnet.magiceden.io/social_metrics/collection/{collection_symbol}'
        return self._request(url)['twitterFollowerCount']

    def get_nft_by_mint_address(self, mint_address: str, use_rarity=False) -> dict:
        """
        Get NFT info by mint address

        :param mint_address: Address
        :param use_rarity:
        :return: nft info dict
        """
        if use_rarity:
            use_rarity = 'true'
        else:
            use_rarity = 'false'

        url = f'https://api-mainnet.magiceden.io/rpc/getNFTByMintAddress/{mint_address}?useRarity={use_rarity}'
        return self._request(url)

    def get_whitelists(self) -> list[dict]:
        """
        Get upcoming whitelist
        :return: list of dicts
        """
        url = 'https://api-mainnet.magiceden.io/whitelists/upcoming'
        return self._request(url)

    def get_listed_nfts(self, collection_symbol) -> list[dict]:
        """
        Get all listings from collections

        :param collection_symbol: symbol name of collection
        :return: list of dict listings info
        """
        q = {
            "$match": {
                "collectionSymbol": collection_symbol
            },
            "$sort": {
                "takerAmount": 1
            },
            "$skip": 0,
            "$limit": 20,
            "status": []
        }
        q = json.dumps(q)
        url = f'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQueryLite?q={q}'
        return self._request(url)['results']

    def get_floor_price(self, collection_symbol) -> float:
        """
        Get real floor price at this moment.
        Get price the cheapest listed nft on this collection.

        :param collection_symbol: collection symbol name
        :return: floor price
        """
        listings = self.get_listed_nfts(collection_symbol)
        if len(listings) == 0:
            return 0
        else:
            return listings[0]['price']

    def get_collections_info(self, collection_symbols_list: list):
        c = ','.join(collection_symbols_list)
        url = 'https://api-mainnet.magiceden.io/rpc/getAggregatedCollectionMetricsBySymbol?' \
              f'edge_cache=true&symbols={c}'
        return self._request(url)

    def get_global_activities(self, collection_symbol: str) -> list[dict]:
        """
        Collections Activity tab data
        Get collection activity log. Exchange, acceptBid, auctionSettled etc.

        :param collection_symbol:
        :return: list of activities
        """

        q = {
            "$match": {
                "txType": {
                    "$in": ["exchange", "acceptBid", "auctionSettled"]
                },
                "source": {
                    "$nin": ["yawww"]
                },
                "collection_symbol": collection_symbol
            },
            "$sort": {
                "blockTime": -1,
                "createdAt": -1
            },
            "$skip": 0,
            "$limit": 50
        }

        q = json.dumps(q)
        url = f'https://api-mainnet.magiceden.io/rpc/getGlobalActivitiesByQuery?q={q}'
        return self._request(url)['results']

    def get_activities_lite(self, collection_symbol, limit=500, offset=0, _type='buy,buyNow') -> list[dict]:
        """
        Collections Analytics tab data

        :param collection_symbol:
        :param limit: 1-500
        :param offset:
        :param _type: buy,buyNow
        :return:
        """
        params = {
            'limit': limit,
            'offset': offset,
            'type': _type
        }

        url = f'https://api-mainnet.magiceden.io/v2/collections/{collection_symbol}/activitiesLite?{params}'
        return self._request(url)

    def get_approx_listings(self, collection_symbol: str, limit=500, offset=0) -> list[dict]:
        """
        Collections Analytics tab data

        :param collection_symbol:
        :param limit: 1-500
        :param offset:
        :return:
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        url = f'https://api-mainnet.magiceden.io/v2/collections/{collection_symbol}/approx_listings?{params}'
        return self._request(url)

    def get_holders(self, collection_symbol) -> dict:
        """
        Collections holder's stats

        :param collection_symbol:
        :return:
        """
        url = f'https://api-mainnet.magiceden.io/v2/collections/{collection_symbol}/holder_stats'
        return self._request(url)

    def get_collection_time_series(self, collection_symbol: str, tdelta: str = '1h') -> list[dict]:
        """
        Collection data per time delta

        :param collection_symbol:
        :param tdelta: 1h | 1d | 6h | 10m
        :return:
        """
        url = f'https://api-mainnet.magiceden.io/rpc/getCollectionTimeSeries/{collection_symbol}?&resolution={tdelta}'
        return self._request(url)

    def get_nfts_by_escrow_owner(self, holder_wallet: str) -> list[dict]:
        """
        Get list of NFTS by holder wallet address

        :param holder_wallet: holder wallet address
        :return:
        """
        url = f'https://api-mainnet.magiceden.io/rpc/getNFTsByEscrowOwner/{holder_wallet}'
        return self._request(url)['results']

    def get_biddings_by_query(self, holder_wallet: str, _type='initializerKey') -> list[dict]:
        """
        Get user biddings

        :param holder_wallet:
        :param _type: initializerKey | bidderPubkey
        :return:
        """
        q = {
            "$match": {},
            "$sort": {
                "createdAt": -1
            }
        }

        q['$match'][_type] = holder_wallet
        q = json.dumps(q)

        url = f'https://api-mainnet.magiceden.io/rpc/getBiddingsByQuery?q={q}'
        return self._request(url)['results']

    def get_user_auction_wallet(self, holder_wallet: str) -> dict:
        url = f'https://api-mainnet.magiceden.io/auctions/wallets/{holder_wallet}'
        return self._request(url)

    def get_user_info(self, holder_wallet: str) -> dict:
        """
        User info. Name, telegram, avatar...
        :param holder_wallet:
        :return:
        """

        url = f'https://api-mainnet.magiceden.io/auth/user/{holder_wallet}'
        return self._request(url)

    def get_user_listings(self, holder_wallet: str) -> list[dict]:
        """
        User exhibited positions

        :param holder_wallet:
        :return:
        """
        url = f'https://api-mainnet.magiceden.io/search_escrows?initializerKey={holder_wallet}'
        return self._request(url)['results']

    def get_user_activity(self, holder_wallet: str) -> list[dict]:
        q = {
            "$match": {
                "$or": [
                    {
                        "seller_address": holder_wallet
                    },
                    {
                        "buyer_address": holder_wallet
                    }
                ],
                "source": {
                    "$nin": ["yawww"]}
            },
            "$sort": {
                "blockTime": -1,
                "createdAt": -1
            },
            "$skip": 0
        }
        q = json.dumps(q)
        url = f'https://api-mainnet.magiceden.io/rpc/getGlobalActivitiesByQuery?q={q}'
        return self._request(url)['results']

    def get_nfts_by_owner(self, holder_wallet: str) -> list[dict]:
        """
        Get user nfts

        :param holder_wallet:
        :return:
        """
        url = f'https://api-mainnet.magiceden.io/rpc/getNFTsByOwner/{holder_wallet}'
        return self._request(url)['results']

    def get_offers_received(self, holder_wallet: str) -> list[dict]:
        url = f'https://api-mainnet.magiceden.io/rpc/m2/getOffersReceived/{holder_wallet}'
        return self._request(url)['results']


