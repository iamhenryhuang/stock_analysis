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
    
    #標示股票價的10%到90%價格區間 (價格抓月收盤量的平均)
    mtk_upper = stocks[('MTK')].resample('ME').mean().quantile(0.9)
    mtk_lower = stocks[('MTK')].resample('ME').mean().quantile(0.1)
    
    #日收益率 使用DataFrame內建pct_change()
    stocks[('MTK','Daily Earnings yield')] = stocks[('MTK')].pct_change(fill_method=None)
    print(stocks[('MTK','Daily Earnings yield')])
    
    # 日收益率的敘述性統計
    print(stocks['MTK', 'Daily Earnings yield'].describe())
    
    # 利用日收益率畫出直方圖(直方圖是用來看數值分散程度的，可大概知道日收益率會落在哪裡)
    stocks[('MTK','Daily Earnings yield')].plot(kind='hist', bins=40, figsize=(10, 10), title='MTK Daily Earings yield')
    plt.xlabel('Daily Earnings Yield')
    plt.ylabel('Frequency')
    plt.show()
        
    # 繪製收盤價線圖
    #stocks.plot(kind="line", grid=True, figsize=(10, 10), title='MTK Close Prices')
    stocks[('MTK')].plot(kind="line", grid=True, figsize=(10, 10), title='MTK Close Prices')
    plt.hlines([mtk_upper, mtk_lower], stocks[('MTK')].index[0], stocks[('MTK')].index[-1])
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show()

except Exception as e:
    print(e)
