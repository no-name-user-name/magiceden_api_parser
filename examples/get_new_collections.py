import time

from magiceden_api import MagicParser

known_collections = []  # better use db
delay = 60

if __name__ == '__main__':
    mp = MagicParser()

    # First init. Load all known collections to database
    collections = mp.get_all_collections()
    [known_collections.append(el['symbol']) for el in collections]

    while 1:
        print(f"[~] Delay {delay} sec...")
        time.sleep(delay)

        collections = mp.get_all_collections()
        for el in collections:
            if el['symbol'] not in known_collections:
                known_collections.append(el['symbol'])
                print("\n[+] New Collection!\n"
                      f"Name: '{el['name']}'\n"
                      f"Link: https://magiceden.io/marketplace/{el['symbol']}\n")

