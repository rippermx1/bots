import json
import sys
from client_socket_manager import ClientSocketManager
from helper import get_klines, get_symbols, get_levels, get_current_price
import asyncio
from binance import Client
import os
from dotenv import load_dotenv
load_dotenv()
from telegram_signal import send_message_to_channel

print(sys.argv)
if len(sys.argv) < 2:
    print('Please enter trading style: scalper, intraday, swing, investor')
    sys.exit()
trading_style = sys.argv[1]
if trading_style == 'scalper':
    interval = '1m'
if trading_style == 'intraday':
    interval = '5m'
if trading_style == 'swing':
    interval = '1h'
if trading_style == 'investor':
    interval = '1d'

client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD"))
bot_api = os.getenv("PIVOTS_BINANCE_BOT")
channel_id = os.getenv("PIVOTS_BINANCE_CHANNEL_ID")
socket_client = ClientSocketManager()
MIN_VOLUME = 3000

def main():    
    socket_client.connect(ClientSocketManager.WS_PIVOT_LEVEL_SCANNER)
    while True:
        symbols = get_symbols(client)
        for symbol in symbols:            
            klines = get_klines(symbol=symbol, interval=interval, client=client)
            if klines.iloc[-1]['volume'] < MIN_VOLUME:
                continue

            levels_df = get_levels(symbol, interval)
            summary = []
            for i in range(len(levels_df)):
                level = float(levels_df.iloc[i].value)
                level_type = str(levels_df.iloc[i].type).capitalize()
                price = get_current_price(client, symbol)
                distance_ptc = round((abs(level - price)/level)*100, 2)
                print(symbol, level, distance_ptc)
                if distance_ptc <= 0.25:
                    summary.append('{} ({}) away {}%'.format(level_type, level, distance_ptc))                    
                    socket_client.send(json.dumps({
                        'symbol': symbol,
                        'interval': interval,
                        'level_type': level_type,
                        'level': level,
                        'price': price,
                        'distance_ptc': distance_ptc
                    }))                                                        
                
            detail = ""
            if len(summary) > 0:
                for s in summary:
                    detail += "{}\n".format(s)                    
                message = "Trading Style: {}\n Symbol: {}\n Timeframe: {}\n Price: {}\n {}".format(trading_style, symbol, interval, price, detail)
                send_message_to_channel(bot_api, channel_id, message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())                    


    


