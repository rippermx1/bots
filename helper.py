import math
from binance import Client
from pandas_ta.core import DataFrame
import pandas as pd
import pandas_ta as ta
import requests as r
import json


def get_levels(symbol, interval):
    base = 'http://127.0.0.1:8001'
    endpoint = 'fractal/levels'
    url = "{}/{}".format(base, endpoint)
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1000
    }
    response = r.post(url, json=params)
    response = json.loads(response.text)
    return DataFrame(response['data'])

def get_symbols(client: Client):
    exclude = ['USDC','BUSD','DAI','UST','TUSD', 'EUR', 'GBP','USDP','PERP']
    s = []
    exchange = client.get_exchange_info()
    for symbol in exchange['symbols']:
        if symbol['status'] == 'TRADING':
            if (not symbol['symbol'].startswith('USDT')) and ('DOWN' not in symbol['symbol']) and ('UP' not in symbol['symbol']) and ('USDT' in symbol['symbol']) and (symbol['baseAsset'] not in exclude):
                s.append(symbol['symbol'])
    return s

def get_balance(client: Client):
    return float([i for i in client.get_account()['balances'] if i['asset'] == 'USDT'][0]['free'])

def get_klines(symbol, interval, client: Client, hist=False, start_str=None):
    if hist:
        data = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_str, limit=1000)
    else:
        data = client.get_klines(symbol=symbol, interval=interval, limit=1000)
    data = DataFrame(data)
    data = data.iloc[:,[0,1,2,3,4,5]]
    data.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    data[['open','high','low','close', 'volume']] = data[['open','high','low','close', 'volume']].astype(float) 
    data['time'] = pd.to_datetime(data['time'], unit='ms')
    return data

def is_volume_growing(klines: DataFrame) -> bool:
    return (klines['volume'].iloc[-1] > klines['volume'].iloc[-2]) & (klines['volume'].iloc[-2] > klines['volume'].iloc[-3]) & (klines['volume'].iloc[-3] > klines['volume'].iloc[-4])

def apply_technical_indicators(klines: DataFrame):
    bollinger_df: DataFrame = ta.bbands(klines['close'], length=6, std=2)
    klines = klines.join(bollinger_df.iloc[:,[2,1,0]]) 
    
    stochcastic_df: DataFrame = ta.stoch(klines['high'], klines['low'], klines['close'], k=9, d=3, smooth_k=3)
    klines = klines.join(stochcastic_df.iloc[:,[0,1]]) 
    
    adx_df: DataFrame = ta.adx(klines['high'], klines['low'], klines['close'], length=9)
    klines = klines.join(adx_df.iloc[:,[0]])

    rsi_df: DataFrame = ta.rsi(klines['close'], length=9)
    klines = klines.join(rsi_df)

    atr_df: DataFrame = ta.atr(klines['high'], klines['low'], klines['close'], length=12)
    klines = klines.join(atr_df)

    klines = klines.dropna()
    klines[['BBU_6_2.0','BBM_6_2.0','BBL_6_2.0','STOCHk_9_3_3','STOCHd_9_3_3', 'ADX_9', 'RSI_9', 'ATRr_12']] = klines[['BBU_6_2.0','BBM_6_2.0','BBL_6_2.0','STOCHk_9_3_3','STOCHd_9_3_3', 'ADX_9', 'RSI_9', 'ATRr_12']].astype(float)            
    return klines

def apply_indicator(klines: DataFrame, indicator: str):
    if indicator == 'stoch':
        stochcastic_df: DataFrame = ta.stoch(klines['high'], klines['low'], klines['close'], k=9, d=2, smooth_k=2)
        klines = klines.join(stochcastic_df.iloc[:,[0,1]])
        klines[['STOCHk_9_2_2','STOCHd_9_2_2']] = klines[['STOCHk_9_2_2','STOCHd_9_2_2']].astype(float)
    if indicator == 'rsi':
        rsi_df: DataFrame = ta.rsi(klines['close'], length=6)
        klines = klines.join(rsi_df)
        klines['RSI_6'] = klines['RSI_6'].astype(float)
    return klines

def get_signal(klines: DataFrame): # for technical indicators
    signal_df: DataFrame = DataFrame() 
    signal_df['adx_1'] = klines['ADX_9'] > 30
    signal_df['adx_2'] = klines['ADX_9'] < 45
    signal_df['bbl'] = klines['close'] < klines['BBL_6_2.0']
    signal_df['stoch_k'] = klines['STOCHk_9_3_3'] < 20
    signal_df['rsi'] = klines['RSI_9'] < 30
    signal_df['signal'] = signal_df['adx_1'] & signal_df['adx_2'] & signal_df['bbl'] & signal_df['stoch_k'] & signal_df['rsi']
    klines = klines.join(signal_df.iloc[:,[5]]) 
    # print(signal_df.tail(1))
    return klines

def round_down(client: Client, symbol, number):
    info = client.get_symbol_info(symbol=symbol)
    step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
    step_size = '%.8f' % step_size
    step_size = step_size.rstrip('0')
    decimals = len(step_size.split('.')[1])
    return math.floor(number * 10 ** decimals) / 10 ** decimals

def round_down_price(client: Client, symbol, number):
    info = client.get_symbol_info(symbol=symbol)
    tick_size = [float(_['tickSize']) for _ in info['filters'] if _['filterType'] == 'PRICE_FILTER'][0]
    tick_size = '%.8f' % tick_size
    tick_size = tick_size.rstrip('0')
    decimals = len(tick_size.split('.')[1])
    return math.floor(number * 10 ** decimals) / 10 ** decimals

def get_lot_size(client: Client, symbol):
    info = client.get_symbol_info(symbol=symbol)
    return [i for i in info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['minQty']

def get_current_price(client: Client, symbol):
    return float(client.get_symbol_ticker(symbol=symbol)['price'])


    '''
lotsize = get_lot_size(client, symbol)
current_price = get_current_price(client, symbol)
stoploss = round(current_price - (klines.iloc[-1]['ATRr_12']*2), len(str(lotsize).split('.')[1]))
qty = round_down(client, symbol, (free_balance / current_price))

order = client.order_limit_buy(symbol=symbol, quantity=qty, price=current_price)
print("[INFO] [ORDER] #{} PLACED".format(order['orderId']))
'''