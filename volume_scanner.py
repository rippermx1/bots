import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from client_socket_manager import ClientSocketManager
from binance import Client
from helper import get_klines, get_symbols, is_volume_growing
load_dotenv()

socket_client = ClientSocketManager()
client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD"))
interval = Client.KLINE_INTERVAL_5MINUTE

def main():
    symbols = get_symbols(client)
    socket_client.connect(ClientSocketManager.WS_VOLUME_SCANNER)
    while True:
        for symbol in symbols:
            klines = get_klines(symbol=symbol, interval=interval, client=client, hist=False)               
            volume_growing = is_volume_growing(klines)
            
            if volume_growing:
                send_msg(symbol, interval)
            print(symbol, volume_growing)
                           

def send_msg(symbol: str, interval: str):
    socket_client.send(json.dumps({
        'symbol': symbol,
        'interval': interval        
    }))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())