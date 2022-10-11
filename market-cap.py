import os
import time

from coinmarketcapapi import CoinMarketCapAPI, Response
from dotenv import load_dotenv
from pandas import DataFrame
load_dotenv()
from database import Database

cmc = CoinMarketCapAPI(os.getenv('COINMARKET_CAP_KEY'))
database = Database()
engine = database.get_engine()

def get_cryptocurrency_listings_latest(cryptocurrency_type="coins", limit=10, convert="USD"):
    r: Response= cmc.cryptocurrency_listings_latest(cryptocurrency_type=cryptocurrency_type, limit=limit, convert=convert)
    return r.data

def get_parsed_cryptocurrency_list(data):
    summary = []
    for a in data:
        summary.append({
            "name": a['name'],
            "symbol": a['symbol'],
            "market_cap": a['quote']['USD']['market_cap'],
            "volume_24h": a['quote']['USD']['volume_24h'],            
            "weight": 0,
            "date": time.time()
        })
    return summary

def get_weighted_cryptocurrency_list(data):
    total_market_cap = 0
    for a in data:
        total_market_cap += a['market_cap']

    for a in data:
        a['weight'] = a['market_cap'] / total_market_cap
        
    return DataFrame(data)

if __name__ == "__main__":
    data = get_cryptocurrency_listings_latest() # From CoinMarketCapAPI
    data = get_parsed_cryptocurrency_list(data) # Summary of data
    data = get_weighted_cryptocurrency_list(data) # Weighted data for each coin
    print(data)
    # data.to_sql('CMK12', con=engine, if_exists='append', index=False)
    # data.to_json()

