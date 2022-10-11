# TIMEFRAME: 1m
# INDICATORS: 
#   - ADX: 12 periods
#   - Bollinger Bands: 6 periods
#   - Stochastic: 9, 3, 3
#   - RSI: 12 periods

# RULES:
#   - ADX > 30 (parameter) and ADX < 45 (parameter)
#   - Close (current session) < Upper Bollinger Band
#   - Stochastic %K < 20

import os
import asyncio
from binance import Client
from pandas import DataFrame
from helper import apply_technical_indicators, get_signal, get_symbols, get_klines
from dotenv import load_dotenv
load_dotenv()
from database import Database

database = Database()
engine = database.get_engine()

async def find_signal(symbol, interval, client: Client):
    try:
        klines = get_klines(symbol=symbol, interval=interval, client=client)
        klines = apply_technical_indicators(klines)  
        klines = get_signal(klines)
        klines['symbol'] = symbol
        klines['interval'] = interval
        print(klines.iloc[-1])         
        
        if klines.iloc[-1]['signal']:
            print('SIGNAL')
            row = [{
                'time': klines.iloc[-1]['time'],
                'open': klines.iloc[-1]['open'],
                'high': klines.iloc[-1]['high'],
                'low': klines.iloc[-1]['low'],
                'close': klines.iloc[-1]['close'],
                'volume': klines.iloc[-1]['volume'],
                'BBU_6_2.0': klines.iloc[-1]['BBU_6_2.0'],
                'BBM_6_2.0': klines.iloc[-1]['BBM_6_2.0'],
                'BBL_6_2.0': klines.iloc[-1]['BBL_6_2.0'],
                'STOCHk_9_3_3': klines.iloc[-1]['STOCHk_9_3_3'],
                'STOCHd_9_3_3': klines.iloc[-1]['STOCHd_9_3_3'],
                'ADX_9': klines.iloc[-1]['ADX_9'],
                'RSI_9': klines.iloc[-1]['RSI_9'],
                'ATRr_12': klines.iloc[-1]['ATRr_12'],
                'signal': 1.0 if klines.iloc[-1]['signal'] else 0.0,
                'symbol': symbol,
                'interval': interval,
                'processed': 0.0
            }]
            df = DataFrame(row)
            df.to_sql("bounce_scalper", con=engine, index=False, if_exists='append')
            return           
    except Exception as e:
        print(e)            


async def main():
    client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD")) 
    symbols = get_symbols(client=client)    
    interval = Client.KLINE_INTERVAL_1MINUTE
    while True:
        try:
            for symbol in symbols:
                client.ping()                                
                await find_signal(symbol, interval, client)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
