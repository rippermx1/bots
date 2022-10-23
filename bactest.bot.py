# Get OHLCV data from Binance
# Get Renko daframe from library
# Get Data To Analisys from Dataframe

#######################################################################################################################################
               # Go Short Signal                                    # Last 4 Renko Brick are Green (Up)
# check (df.close[-1] < df.close[-2]) and (df.close[-2] > df.close[-3] and df.close[-3] > df.close[-4] and df.close[-4] > df.close[-5])
# stochastic ((%K[-1] > 95) and (%D[-1] > 95)) and ((%K[-2] > 95) and (%D[-2] > 95)) and ((%K[-3] > 95) and (%D[-3] > 95)) and ((%K[-4] > 95) and (%D[-4] > 95)) and (%K[-1] < %D[-1])
#######################################################################################################################################
               # Go Long Signal                                    # Last 4 Renko Brick are Red (Down)
# check (df.close[-1] > df.close[-2]) and (df.close[-2] < df.close[-3] and df.close[-3] < df.close[-4] and df.close[-4] < df.close[-5])
# stochastic ((%K[-1] < 5) and (%D[-1] < 5)) and ((%K[-2] < 5) and (%D[-2] < 5)) and ((%K[-3] < 5) and (%D[-3] < 5)) and ((%K[-4] < 5) and (%D[-4] < 5)) and (%K[-1] > %D[-1])
#######################################################################################################################################

from pandas import DataFrame


def get_signals(df: DataFrame):
    for i in range(len(df)):
        if (df.iloc[i-1].close < df.close[i-2]) and (df.close[-2] > df.close[-3] and df.close[-3] > df.close[-4] and df.close[-4] > df.close[-5]) and ((%K[-1] > 95) and (%D[-1] > 95)) and ((%K[-2] > 95) and (%D[-2] > 95)) and ((%K[-3] > 95) and (%D[-3] > 95)) and ((%K[-4] > 95) and (%D[-4] > 95)) and (%K[-1] < %D[-1]):
            df.loc[df.index[i], 'signal'] = -1
        elif (df.close[-1] > df.close[-2]) and (df.close[-2] < df.close[-3] and df.close[-3] < df.close[-4] and df.close[-4] < df.close[-5]) and ((%K[-1] < 5) and (%D[-1] < 5)) and ((%K[-2] < 5) and (%D[-2] < 5)) and ((%K[-3] < 5) and (%D[-3] < 5)) and ((%K[-4] < 5) and (%D[-4] < 5)) and (%K[-1] > %D[-1]):
            df.loc[df.index[i], 'signal'] = 1
        else:
            df.loc[df.index[i], 'signal'] = 0
