# Get pick of volume (Extrema of volume for a given period N), If timeframe is 5m, then N = 12, if timeframe is 1h, then N = 24, if timeframe is 1d, then N = 30
# Get klines for tha pick
# Draw a line (control level) on the chart for High and Low for that volume pick

import os
from dotenv import load_dotenv
load_dotenv()
from binance import AsyncClient, BinanceSocketManager
import asyncio
from pandas import DataFrame

async def main():
    symbol = 'BTCUSDT'
    client = await AsyncClient.create(api_key=os.getenv("API_KEY_PROD"), api_secret=os.getenv("SECRET_KEY_PROD"))
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket(symbol=symbol)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            # is buyer maker = true -> SELL
            # is buyer maker = false -> BUY
            side = 'SELL' if res['m'] else 'BUY'    
            
            # print("SYMBOL:{} PRICE:{} QTY:{} TIME:{} SIDE:{}".format(res['s'], str(res['p']), str(res['q']), str(res['T']), side))
            print("SYMBOL:{} VOLUME:{} TIME:{}".format(res['s'] , res['q'], res['T']))
    await client.close_connection()    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())