# ROBOT BASIS
* API Integration (Binance)
* Get Symbols 
* Get OHLCV
* Apply Indicators
* Get Signals

# API Integration (Binance)
* Get API Key and Secret Key from ENV
* TODO:
    - Integrates with other exchanges (FTX, Bitget, etc)

# Get Symbols
* Function to get symbols from Binance
* Returns a list of symbols from Binance
* Use array str as input to filter symbols



# Donchian Channel + STOCH + EMAs (30 min)
* Donchian Channel: 20 periods 
* STOCH: 14, 3, 2
* EMAs: 3, 4

# Conditions (LONG)
* Close distance from lower band < 1.5%
* K < 20 and D < 20
* K > D
* Close < EMA 3 and Close < EMA 4

# Conditions (SHORT)
* Close distance from upper band < 1.5%
* K > 80 and D > 80
* K < D
* Close > EMA 3 and Close > EMA 4

# For any time i have an idea:
# Feature 
    * Any new functionallity to the product
# Proposal
    * Why should we implement this feature?
# Value
    * What value does this feature bring to the product?

# Idea [N°1]:
* Feature: Alert when a symbol is near to technical Support or Resistance (ema, sma, vwap, etc)
* Proposal: This feature will help to identify when a symbol is near to a technical support or resistance, so we can take a position in the direction of the trend.
* Value: Save Research Time to identify Manually when a symbol is near to a technical support or resistance.