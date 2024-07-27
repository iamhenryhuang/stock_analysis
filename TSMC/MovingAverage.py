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
    
    # 計算 7、14、21 日均線值
    for x in [7, 14, 21]:
        stocks[f'MA{x}'] = stocks['TSMC'].rolling(window=x).mean()
    
    # 取得特定日期範圍內的數據
    selected_data = stocks.loc['2024-01-26':'2024-07-26', ['TSMC', 'MA7', 'MA14', 'MA21']]
    
    # 繪製圖表
    selected_data.plot(kind='line', grid=True, figsize=(10, 10), title='TSMC Close Prices and Moving Averages (2024-01-26 to 2024-07-26)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(['Close Price', '7-Day MA', '14-Day MA', '21-Day MA'])
    plt.show()

except Exception as e:
    print(e)


# note
"""
移動平均線，是算出一定期間的價格平均值，並將之連成的線圖。
簡單移動平均乃合計n期間的收盤價，然後再除以n計算得出。計算時會計算最近的n期間，觀看該計算數值每一天的變動
"""
