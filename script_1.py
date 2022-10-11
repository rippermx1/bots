import os
import sys
import asyncio
import signal
from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv
load_dotenv()

symbol = sys.argv[1]
entry_price = float(sys.argv[2])
entry_order_id = sys.argv[3]
stop_order_id = sys.argv[4]
qty = float(sys.argv[5])

stop_loss_margin = 0.995 # 0.5% stop loss margin
take_profit_margin = 1.0085 # 0.85% take profit margin

take_profit_bid = entry_price * take_profit_margin
stop_loss_bid = entry_price * stop_loss_margin

async def main():
    client = await AsyncClient.create(api_key=os.getenv("API_KEY_PROD"), api_secret=os.getenv("SECRET_KEY_PROD"))
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket(symbol=symbol)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)
            if float(res["p"]) >= take_profit_bid:
                print("Take profit")
                await client.cancel_order(symbol=symbol, orderId=stop_order_id)
                await client.create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)                
                break
            if float(res["p"]) <= stop_loss_bid:
                print("Stop loss")                                
                break      

    await client.close_connection()
    os.kill(os.getppid(), signal.SIGTERM)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())