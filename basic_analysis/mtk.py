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

    # 構建包含收盤價的 DataFrame
    stocks = pd.concat([df_2454['Close']], axis=1, keys=["MTK"])
    
    #標示股票價的 10% 到 90% 價格區間 (價格抓月收盤量的平均)
    #stocks = pd.concat([df_2454['Close'].resample('ME').mean()], axis=1, keys=["MTK"])
    mtk_upper = stocks[('MTK')].quantile(0.9)
    mtk_lower = stocks[('MTK')].quantile(0.1)
    #print("Upper: %s, Lower: %s" % (mtk_upper, mtk_lower))
    
    #日收益率 法一 公式((今天的價格 - 昨天的價格) / 昨天的價格)
    """
    stocks[('MTK','Daily Earnings yield')] = ((stocks[('MTK')] - stocks[('MTK')].shift(1)) / stocks[('MTK')].shift(1))
    print(stocks[('MTK','Daily Earnings yield')])
    """
    #日收益率 法二 使用DataFrame內建pct_change()
    stocks[('MTK','Daily Earnings yield')] = stocks[('MTK')].pct_change(fill_method=None)
    #print(stocks[('MTK','Daily Earnings yield')])
    
    # 利用日收益率畫出直方圖(直方圖是用來看數值分散程度的，可大概知道日收益率會落在哪裡)
    stocks[('MTK','Daily Earnings yield')].plot(kind='hist', bins=40, figsize=(10, 10), title='MTK Daily Earings yield')
    plt.xlabel('Daily Earnings Yield')
    plt.ylabel('Frequency')
    plt.show()
    
    # 日收益率的敘述性統計
    #print(stocks['MTK', 'Daily Earnings yield'].describe())
    #取特定日收益率的敘述性統計 e.g. std()
    #stocks[('MTK','Daily Earnings yield')].std()
    
    #算出均線
    #print(stocks[('MTK')].rolling(3).sum())
    
    #計算 7、14、21 日均線值
    for x in [7, 14, 21]:
        stocks[('MTK', f'MA{x}')] = stocks[('MTK')].rolling(window=x).mean()
    
    # 繪製收盤價線圖
    """
    #stocks.plot(kind="line", grid=True, figsize=(10, 10), title='MTK Close Prices')
    stocks[('MTK')].plot(kind="line", grid=True, figsize=(10, 10), title='MTK Close Prices')
    plt.hlines([mtk_upper, mtk_lower], stocks[('MTK')].index[0], stocks[('MTK')].index[-1])
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show()
    """
    
    # 繪製移動平均線圖表
    """
    plt.figure(figsize=(10, 10))
    plt.plot(stocks[('MTK', 'MA7')], label='7-Day MA')
    plt.plot(stocks[('MTK', 'MA14')], label='14-Day MA')
    plt.plot(stocks[('MTK', 'MA21')], label='21-Day MA')
    plt.hlines([mtk_upper, mtk_lower], stocks.index[0], stocks.index[-1], colors=['r', 'g'])
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('MTK Moving Averages')
    plt.legend()
    plt.grid(True)
    plt.show()
    """
    
except Exception as e:
    print(e)