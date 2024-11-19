import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# 獲取 Yahoo Finance 數據的函數
def get_yahoo_finance_data(symbol, start, end):
    # 使用 yfinance 下載數據
    df = yf.download(symbol, start=start, end=end)
    
    # 確保數據包含必要的欄位
    if 'Close' not in df.columns:
        raise Exception("Failed to fetch Close price data")
    
    return df

# 定義日期範圍
start = "2015-01-01"
end = dt.datetime.now().strftime('%Y-%m-%d')

try:
    # 獲取比特幣 (BTC-USD) 的數據
    df_btc = get_yahoo_finance_data('BTC-USD', start, end)
    
    # 建立收盤價資料表
    stocks = pd.DataFrame(df_btc['Close'])
    stocks.rename(columns={'Close': 'Bitcoin'}, inplace=True)
    
    # 計算 21 日均線值
    stocks['MA21'] = stocks['Bitcoin'].rolling(window=21).mean()
    
    # 選取指定日期範圍內的數據
    selected_data = stocks.loc['2024-06-07':'2024-07-07', ['Bitcoin', 'MA21']]
    
    # 繪製比特幣收盤價及均線圖表
    selected_data.plot(kind='line', grid=True, figsize=(10, 6), title='Bitcoin Close Prices and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(['Close Price', '21-Day MA'])
    plt.grid(True)
    plt.show()

except Exception as e:
    print(e)


#note
"""
當收盤價從等於均價後，漸漸大於均價 -> 買點 可以做多
當收盤價漸漸下跌，且準備等於均價 -> 賣點 可以做空
"""
