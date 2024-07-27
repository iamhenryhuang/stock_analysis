import requests
import pandas as pd
import datetime as dt
import time
import io
import matplotlib.pyplot as plt

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

    stocks = pd.concat([df_2330['Close']], axis=1, keys=["TSMC"])
    
    #標示股票價的10%到90%價格區間 (價格抓月收盤量的平均)
    tsmc_upper = stocks[('TSMC')].resample('ME').mean().quantile(0.9)
    tsmc_lower = stocks[('TSMC')].resample('ME').mean().quantile(0.1)
    
    # 繪製收盤價線圖
    #stocks.plot(kind="line", grid=True, figsize=(10, 10), title='MTK Close Prices')
    stocks[('TSMC')].plot(kind="line", grid=True, figsize=(10, 10), title='TSMC Close Prices')
    plt.hlines([tsmc_upper, tsmc_lower], stocks[('TSMC')].index[0], stocks[('TSMC')].index[-1])
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show()

except Exception as e:
    print(e)
