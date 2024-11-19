import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

def get_yahoo_finance_data(symbol, start, end):
    # 透過 yfinance 下載數據
    df = yf.download(symbol, start=start, end=end)
    
    # 確保數據包含必要的欄位
    if 'Close' not in df.columns:
        raise Exception("Failed to fetch Close price data")
    
    return df

start = "2020-01-01"
#end = dt.datetime.now().strftime('%Y-%m-%d')
end = "2024-11-20"

try:
    # 獲取台積電 (2330.TW) 的數據
    df_2330 = get_yahoo_finance_data('2330.TW', start, end)

    # 建立收盤價資料表
    stocks = pd.DataFrame(df_2330['Close'])
    stocks.rename(columns={'Close': 'TSMC'}, inplace=True)
    
    # 計算日收益率
    stocks['Daily Earnings Yield'] = stocks['TSMC'].pct_change()

    # 列印日收益率數據
    print(stocks['Daily Earnings Yield'])
    
    # 日收益率的敘述性統計
    print(stocks['Daily Earnings Yield'].describe())
    
    # 繪製日收益率的直方圖
    stocks['Daily Earnings Yield'].plot(
        kind='hist', 
        bins=40, 
        figsize=(10, 6), 
        title='TSMC Daily Earnings Yield'
    )
    plt.xlabel('Daily Earnings Yield')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

except Exception as e:
    print(e)
