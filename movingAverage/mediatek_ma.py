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

start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

try:
    time.sleep(5)

    df_2454 = get_yahoo_finance_data('2454.TW', start, end)

    stocks = pd.concat([df_2454['Close']], axis=1, keys=["MTK"])
    
    # 計算 7、14、21 日均線值
    for x in [7, 14, 21]:
        stocks[f'MA{x}'] = stocks['MTK'].rolling(window=x).mean()
    
    # 取得特定日期範圍內的數據
    selected_data = stocks.loc['2023-07-01':'2024-07-01', ['MTK', 'MA7', 'MA14', 'MA21']]
    
    # 繪製圖表
    selected_data.plot(kind='line', grid=True, figsize=(10, 10), title='MTK Close Prices and Moving Averages (2023-07-01 to 2024-07-01)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(['Close Price', '7-Day MA', '14-Day MA', '21-Day MA'])
    plt.show()

except Exception as e:
    print(e)
