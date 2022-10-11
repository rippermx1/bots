import os
from dotenv import load_dotenv
load_dotenv()
from binance import AsyncClient, BinanceSocketManager
import asyncio
from pandas import DataFrame

from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

# Group sell volume by price
# Group buy volume by price
# Get total volume for each price


async def main():
    symbol = 'BTCUSDT'
    table_title = 'Time and Sales: {}'.format(symbol)
    table = Table(title=table_title)
    
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
            side_color = 'red' if res['m'] else 'green'
            
            # print("SYMBOL:{} PRICE:{} QTY:{} TIME:{} SIDE:{}".format(res['s'], res['p'], res['q'], res['T'], side))  
            
            table.add_column("TIME", justify="right", style=side_color)
            table.add_column("PRICE",justify="right", style=side_color)
            table.add_column("QTY", justify="right", style=side_color)
            table.add_column("SIDE", justify="right", style=side_color)

            table.add_row(str(res['T']), str(res['p']), str(res['q']), side)   
            panel_group = Group(table)
            print(Panel(panel_group))       

    await client.close_connection()    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())