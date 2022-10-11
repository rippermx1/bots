# 1. get_klines (daily)
# 2. Quote asset volume
# 3. Quote asset volume > 1000
# .  get_order_book (symbol) -> return dict A (Only Limit orders)
# .  for each bid in A:
# 4. Create market order
# 4.1. Wait for order to be filled
# 4.2. Get order info
# Quote asset volume < 1000 => avg daily volume for buy market order quantity
# Check balance (volume) neccesary to buy market order


# Check order book before market order creation, check liquidity by level
# Place stop market order at 3% from entry price, then if price goes above profit price (3%), cancel stop order and place profit market order

import os
from dotenv import load_dotenv
load_dotenv()
from binance import Client
import pandas as pd
from helper import get_lot_size, get_current_price, round_down, get_balance, round_down_price

stop_loss_margin = 0.995 # 0.5% stop loss margin
min_to_invest = 25

def place_order(symbol):
    entry_order = None
    stop_order = None
    client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD"))

    balance = get_balance(client)
    print(balance)
    
    if balance > min_to_invest:
        order_book = get_order_book(client, symbol)
        for i in range(len(order_book)):
            print("level {}".format(i))
            print("bid {}".format(order_book.iloc[i].bids))
            print("ask {}".format(order_book.iloc[i].asks))
            ask_price = float(order_book.iloc[i].asks[0])
            ask_liquidity = float(order_book.iloc[i].asks[1])
            qty = round_down(client, symbol, (min_to_invest / ask_price))
            print("qty {}".format(qty))        
            if qty < ask_liquidity:
                entry_order = client.create_order(symbol=symbol, side="BUY", type="LIMIT", quantity=qty, timeInForce='GTC', price=ask_price)
                print("entry_order {}".format(entry_order))      
                if entry_order is not None:
                    qty = round_down(client, symbol, float(entry_order["fills"][0]["qty"])-float(entry_order["fills"][0]["commission"]))                    
                    stop_price = round_down_price(client, symbol, (ask_price * stop_loss_margin))
                    stop_order = client.create_order(symbol=symbol, side="SELL", type='STOP_LOSS_LIMIT', quantity=qty, price=stop_price, stopPrice=stop_price, timeInForce='GTC')
                    print("stop_order {}".format(stop_order))                                    
                break
            else:
                print("Not enough liquidity")
                break        
    return entry_order, stop_order  

def get_order_book(client: Client, symbol):   
    return pd.DataFrame(client.get_order_book(symbol=symbol, limit=10))