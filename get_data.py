import time
import requests
import pandas as pd

def resample_data(df, integer, htf):
    tf_mapper = {'MIN':'T','HOUR':'H','DAY':'D','WEEK':'W','MONTH':'M'}
    htf = str(integer)+tf_mapper[htf]
    df['low']    = df.low.resample(htf).min()
    df['high']   = df.high.resample(htf).max()
    df['open']   = df.open.resample(htf).first()
    df['close']  = df.close.resample(htf).last()
    df['volume'] = df.volume.resample(htf).sum()
    return df.dropna().reset_index(drop=True)

def request_data(timeframe, pair, start, end):
    url = "https://poloniex.com/public?command=returnChartData&currencyPair={0}&start={1}&end={2}&period={3}"
    url = url.format(pair, start, end, timeframe)
    response = requests.get(url)
    df = pd.DataFrame(response.json())
    df['date'] = pd.to_datetime(df.date, unit='s')
    return df

"""
HOW TO USE
- We're going to request 5 minute candles of ETH on the BTC 
  market from Poloniex and resample them to 3 daily candles
"""


pair = 'BTC_ETH'                # MARKET_TICKER
timeframe = 60*5                # 5 minute candles
end = time.time()               # From now
start = end-(int(86400*365*3))  # To 3 years ago 

df = request_data(timeframe, pair, start, end)
df = df.set_index(df['date'])
df = resample_data(df, 3, 'DAY')
