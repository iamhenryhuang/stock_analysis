import requests
import pandas as pd
import datetime as dt
import time
import io
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, message="Period with BDay freq is deprecated and will be removed in a future version. Use a DatetimeIndex with BDay freq instead.")

def get_yahoo_finance_data(symbol, start, end):
    start_timestamp = int(start.timestamp())
    end_timestamp = int(end.timestamp())
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    # 解析 CSV 數據
    data = response.content.decode('utf-8')
    df = pd.read_csv(io.StringIO(data))
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    return df

start = dt.datetime(2020, 1, 1)
end = dt.datetime.now()

try:
    time.sleep(0.5)

    df_2330 = get_yahoo_finance_data('2330.TW', start, end)

    # 構建包含所需價格的 DataFrame
    stocks = df_2330[['High', 'Low', 'Close']].copy()
    stocks.columns = pd.MultiIndex.from_product([['TSMC'], stocks.columns])
    
    # 計算威廉指數
    highest_high = stocks[('TSMC', 'High')].rolling(window=14).max()
    lowest_low = stocks[('TSMC', 'Low')].rolling(window=14).min()
    stocks[('TSMC', 'William')] = ((highest_high - stocks[('TSMC', 'Close')]) / (highest_high - lowest_low)) * -100
    
    # 繪製威廉指數
    stocks['TSMC'].loc['2024-01-01':'2024-07-01', 'William'].plot(kind='line', grid=True, figsize=(10, 10), title='TSMC William %R (2024-01-01 - 2024-07-01)')
    plt.xlabel('Date')
    plt.ylabel('William %R')
    plt.show()

except Exception as e:
    print(e)
    
# note
"""
威廉指標可以幫助判斷目前價格是否處於超買或超賣，並抓出股價轉折點，找到適合的進出場時機。
威廉指標的公式主要是透過最新收盤價與最近一段週期內的最高價與最低價來計算。
W%R 公式 = （N 日最高價 - 收盤價）÷（N 日最高價 - N 日最低價）× 100% ×（-1）
RSV 公式 =（收盤價 - N 日最低價）÷（N 日最高價 - N 日最低價）× 100
根據上述公式，可以得知威廉指標計算出來的值，會落在 0～-100 之間，當數值愈大，代表市場「超買」程度愈大﹔反之，數值越小代表市場「超賣」程度愈大。
"""
