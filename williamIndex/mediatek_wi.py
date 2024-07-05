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

start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

try:
    time.sleep(5)

    df_2454 = get_yahoo_finance_data('2454.TW', start, end)

    # 構建包含所需價格的 DataFrame
    stocks = df_2454[['High', 'Low', 'Close']].copy()
    stocks.columns = pd.MultiIndex.from_product([['MTK'], stocks.columns])
    
    # 計算威廉指數
    highest_high = stocks[('MTK', 'High')].rolling(window=14).max()
    lowest_low = stocks[('MTK', 'Low')].rolling(window=14).min()
    stocks[('MTK', 'William')] = ((highest_high - stocks[('MTK', 'Close')]) / (highest_high - lowest_low)) * -100
    
    # 繪製威廉指數
    stocks['MTK'].loc['2021-11':'2021-12', 'William'].plot(kind='line', grid=True, figsize=(10, 10), title='MTK William %R (Nov 2021 - Dec 2021)')
    plt.xlabel('Date')
    plt.ylabel('William %R')
    plt.show()

except Exception as e:
    print(e)
