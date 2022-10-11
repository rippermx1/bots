import subprocess
import os
from binance import Client

from helper import round_down

client = Client(os.getenv("API_KEY_PROD"), os.getenv("SECRET_KEY_PROD"))

# For Linux: gnome-terminal -e "python3 /path/to/script.py"
def open_monitor_terminal(entry_order, stop_order):
    symbol = entry_order["symbol"]
    entry_price = float(entry_order["fills"][0]["price"])
    entry_order_id = entry_order["orderId"]
    stop_order_id = stop_order["orderId"]
    qty = round_down(client, symbol, float(entry_order["fills"][0]["qty"])-float(entry_order["fills"][0]["commission"]))
    
    subprocess.Popen("start cmd /k python D:\CVA_Capital\Bots\script_1.py {} {} {} {} {}".format(symbol, entry_price, entry_order_id, stop_order_id, qty), shell=True)

# subprocess.call('python D:\CVA_Capital\Bots\script_1.py BTCUSDT', creationflags=subprocess.CREATE_NEW_CONSOLE)
# subprocess.call('python D:\CVA_Capital\Bots\script_2.py ETHUSDT', creationflags=subprocess.CREATE_NEW_CONSOLE)
# subprocess.Popen("start cmd /k python D:\CVA_Capital\Bots\script_2.py", shell=True)    