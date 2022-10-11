import os
from dotenv import load_dotenv
load_dotenv()
import ccxt
from helper import get_volume_by_risk

# print(ccxt.exchanges)

ftx = ccxt.ftx({
    'apiKey': os.getenv("API_KEY_FTX"),
    'secret': os.getenv("SECRET_KEY_FTX")
})

ftx.load_markets()

# print(ftx.fetch_markets()[0])

futures = [i for i in ftx.fetch_markets() if i['future'] and i['active']]
swaps = [i for i in ftx.fetch_markets() if i['swap'] and i['active']]
print(swaps[0])

# print(ftx.fetch_ticker('BTC-PERP'))
# print(ftx.fetch_balance())

result = get_volume_by_risk(2000, 5)
print(result)