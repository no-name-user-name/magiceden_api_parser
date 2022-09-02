import json
from pprint import pprint

from magicapi import MagicParser
from urllib.parse import quote, urlencode


if __name__ == '__main__':
    mp = MagicParser(profile='tests', driver_headless=True)

    # pprint(mp.get_featured_carousels())
    # pprint(mp.get_featured_collections_carousels())
    # pprint(mp.get_magiceden_volumes())
    # pprint(mp.get_all_collections())
    # pprint(mp.get_all_organizations())
    # print(mp.get_popular_collections(limit=1, period='1d'))

    # pprint(mp.get_all_organizations())
    # pprint(mp.get_price())
    # pprint(mp.get_launchpad_collections())
    # pprint(mp.get_auctions('finished'))
    # pprint(mp.get_auctions('finished'))
    # pprint(mp.get_drops(top=15))

    # symbols = ["degods"]
    # pprint(mp.get_collections_witch_symbols(symbols))
    # pprint(mp.get_auction_by_symbol('ttg_sanctified'))
    # pprint(mp.check_collection_scam_flag(symbol='acidmonkeys'))
    # print(mp.get_twitter_followers(symbol='acidmonkeys'))
    # pprint(mp.get_listed_nfts('acidmonkeys'))
    # pprint(mp.get_floor_price('acidmonkeys'))
    # pprint(mp.get_global_activities('acidmonkeys'))
    # pprint(mp.get_activities_lite('acidmonkeys'))
    # pprint(mp.get_approx_listings('acidmonkeys'))
    # pprint(mp.get_holders_stats('acidmonkeys'))
    # pprint(mp.get_collection_time_series('acidmonkeys'))

    # pprint(mp.get_nfts_by_escrow_owner('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4'))
    # pprint(mp.get_biddings_by_query('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4', _type='initializerKey'))
    # pprint(mp.get_biddings_by_query('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4', _type='bidderPubkey'))
    # pprint(mp.get_user_info('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4'))
    # pprint(mp.get_user_listings('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4'))
    # pprint(mp.get_user_activity('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4'))
    pprint(mp.get_nfts_by_owner('D2nm4ESk44NwZfHexvrTWSg3cYGWQPxDHmvtMmvU8Ry4'))
