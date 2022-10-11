import os
import asyncio
from binance import Client
from helper import get_symbols, get_klines, apply_indicator, get_levels, get_current_price
from dotenv import load_dotenv
load_dotenv()
from database import Database
from pandas import DataFrame

database = Database()
engine = database.get_engine()
ABOVE = 'ABOVE'
BELOW = 'BELOW'
treshold = 0.1

async def find_signal(symbol, interval_pivots, interval_entry, client: Client):
    try:
        print(symbol)
        fractal_levels = get_levels(symbol=symbol, interval=interval_pivots)
        for i in range(len(fractal_levels)):
            level = float(fractal_levels.iloc[i].value)
            price = get_current_price(client=client, symbol=symbol)
            distance_ptc = round((abs(level - price)/level)*100, 2)
            # position = ABOVE if price > level else BELOW

            if distance_ptc <= treshold:
                klines = get_klines(symbol=symbol, interval=interval_entry, client=client)        
                klines = apply_indicator(klines, "stoch") # STOCH (9, 2, 2)
                klines = apply_indicator(klines, "rsi") # RSI (6)
            
                # If rsi < 30 and stochastic %K < 20 and close near fractal pivot (less than 0.10%) , then buy 
                if klines.iloc[-1]['RSI_6'] < 30 and klines.iloc[-1]['STOCHk_9_2_2'] < 20 and klines.iloc[-1]['volume'] >= 1000:
                    row = [{
                        'time': klines.iloc[-1]['time'],
                        'open': klines.iloc[-1]['open'],
                        'high': klines.iloc[-1]['high'],
                        'low': klines.iloc[-1]['low'],
                        'close': klines.iloc[-1]['close'],
                        'volume': klines.iloc[-1]['volume'],
                        'STOCHk_9_2_2': klines.iloc[-1]['STOCHk_9_2_2'],
                        'STOCHd_9_2_2': klines.iloc[-1]['STOCHd_9_2_2'],
                        'RSI_6': klines.iloc[-1]['RSI_6'],                        
                        'symbol': symbol,
                        'interval_pivots': interval_pivots,
                        'interval_entry': interval_entry,
                        'pivot_level': level,
                        'distance_ptc': distance_ptc,
                        'processed': 0
                    }]
                    df = DataFrame(row)
                    print(df)
                    df.to_sql("pivot_level_scalper", con=engine, index=False, if_exists='append')                           
    except Exception as e:
        print(e)            


async def main():
    client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD")) 
    symbols = get_symbols(client=client)    
    interval_pivots = Client.KLINE_INTERVAL_5MINUTE
    interval_entry = Client.KLINE_INTERVAL_1MINUTE
    while True:
        try:
            for symbol in symbols:
                client.ping()                                
                await find_signal(symbol, interval_pivots, interval_entry, client)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
