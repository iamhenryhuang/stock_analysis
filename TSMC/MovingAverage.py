import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def get_yahoo_finance_data(symbol, start, end):
    # 透過 yfinance 下載數據
    df = yf.download(symbol, start=start, end=end)
    
    # 確保數據包含必要的欄位
    if 'Close' not in df.columns:
        raise Exception("Failed to fetch Close price data")
    
    return df

# 定義日期範圍
start = "2020-01-01"
end = "2024-11-20"

try:
    # 獲取台積電 (2330.TW) 的數據
    df_2330 = get_yahoo_finance_data('2330.TW', start, end)

    # 建立收盤價資料表
    stocks = pd.DataFrame(df_2330['Close'])
    stocks.rename(columns={'Close': 'TSMC'}, inplace=True)
    
    # 計算 7、14、21 日均線值
    for x in [7, 14, 21]:
        stocks[f'MA{x}'] = stocks['TSMC'].rolling(window=x).mean()
    
    # 取得特定日期範圍內的數據
    selected_data = stocks.loc['2024-01-26':'2024-11-20', ['TSMC', 'MA7', 'MA14', 'MA21']]
    
    # 繪製圖表
    selected_data.plot(kind='line', grid=True, figsize=(10, 6), title='TSMC Close Prices and Moving Averages (2024-01-26 to 2024-11-20)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(['Close Price', '7-Day MA', '14-Day MA', '21-Day MA'])
    plt.grid(True)
    plt.show()

except Exception as e:
    print(e)
