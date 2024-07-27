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
        
    #日收益率 使用DataFrame內建pct_change()
    stocks[('TSMC','Daily Earnings yield')] = stocks[('TSMC')].pct_change(fill_method=None)
    print(stocks[('TSMC','Daily Earnings yield')])
    
    # 日收益率的敘述性統計
    print(stocks['TSMC', 'Daily Earnings yield'].describe())
    
    # 利用日收益率畫出直方圖(直方圖是用來看數值分散程度的，可大概知道日收益率會落在哪裡)
    stocks[('TSMC','Daily Earnings yield')].plot(kind='hist', bins=40, figsize=(10, 10), title='TSMC Daily Earings yield')
    plt.xlabel('Daily Earnings Yield')
    plt.ylabel('Frequency')
    plt.show()

except Exception as e:
    print(e)
