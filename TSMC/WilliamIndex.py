import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# 獲取 Yahoo Finance 數據的函數
def get_yahoo_finance_data(symbol, start, end):
    # 使用 yfinance 下載數據
    df = yf.download(symbol, start=start, end=end)
    
    # 確保數據包含必要的欄位
    if not all(col in df.columns for col in ['High', 'Low', 'Close']):
        raise Exception("Failed to fetch required data columns (High, Low, Close)")
    
    return df

# 定義日期範圍
start = "2020-01-01"
end = dt.datetime.now().strftime('%Y-%m-%d')

try:
    # 獲取台積電 (2330.TW) 的數據
    df_2330 = get_yahoo_finance_data('2330.TW', start, end)

    # 構建包含所需價格的 DataFrame
    stocks = df_2330[['High', 'Low', 'Close']].copy()
    stocks.columns = pd.MultiIndex.from_product([['TSMC'], stocks.columns])
    
    # 計算威廉指數
    highest_high = stocks[('TSMC', 'High')].rolling(window=14).max()
    lowest_low = stocks[('TSMC', 'Low')].rolling(window=14).min()
    stocks[('TSMC', 'William')] = ((highest_high - stocks[('TSMC', 'Close')]) / (highest_high - lowest_low)) * -100
    
    # 繪製威廉指數
    stocks['TSMC'].loc['2024-01-01':'2024-11-20', 'William'].plot(
        kind='line', 
        grid=True, 
        figsize=(10, 6), 
        title='TSMC William %R (2024-01-01 - 2024-11-20)'
    )
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
