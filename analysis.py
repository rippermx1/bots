import pandas as pd
from helper import get_klines
from database import Database
from binance import Client
import os
from dotenv import load_dotenv
load_dotenv()

client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD"))
engine = Database().get_engine()
df = pd.read_sql_query("SELECT * FROM bounce_scalper", engine)

demo_balance = 50
orders = []
win = 0
loss = 0
fee = 0.999 # 0.1% fee
stop_loss_margin = 0.995 # 0.5% stop loss margin
profit_margin = 1.0075 # 0.75% profit margin

for i in range(len(df)):
    row = df.iloc[i]
    print(row.symbol, row.time)
    
    minutes = 0
    qty = 0
    
    # Risk reward ratio = 1:1
    entry_price = row.close
    stop_loss = entry_price * stop_loss_margin # 2% loss
    take_profit = entry_price * profit_margin # 2% profit

    demo_balance *= fee
    
    klines = get_klines(symbol=row.symbol, interval=row.interval, client=client, hist=True, start_str=str(row.time))
    klines.drop(index=df.index[0], axis=0, inplace=True)

    # Simulate track of the trade
    for i in range(len(klines)):
        minutes += 1
        # print(klines.iloc[i])
        if klines.iloc[i].close <= stop_loss or klines.iloc[i].low <= stop_loss:
            orders.append({
                "symbol": row.symbol, 
                "type": "STOP_LOSS", 
                "entry_price": entry_price,
                "stop_price": stop_loss,
                "take_profit": take_profit,
                "time": klines.iloc[i].time,
                "minutes_elapsed": minutes})
            loss += 1
            demo_balance *= fee
            demo_balance *= stop_loss_margin
            print("Stop loss triggered")
            break
        if klines.iloc[i].close >= take_profit:
            orders.append({
                "symbol": row.symbol, 
                "type": "TAKE_PROFIT", 
                "entry_price": entry_price,
                "stop_price": stop_loss,
                "take_profit": take_profit,
                "time": klines.iloc[i].time,
                "minutes_elapsed": minutes})
            win += 1
            demo_balance *= fee
            demo_balance *= profit_margin
            print("Take profit triggered")
            break
    print("Balance: {}".format(demo_balance))
    print("Win: {} | Loss: {}".format(win, loss, ))
    print("win ptc: {}%".format((win / (win + loss)) * 100))
    print("loss ptc: {}%".format((loss / (win + loss)) * 100))
    print("Total: {}".format(win + loss))
    print("minutes: {}".format(minutes))




# entry_price - (row.ATRr_12 * 2) # 2 times ATR
# entry_price + (row.ATRr_12 * 2) # 2 times ATR