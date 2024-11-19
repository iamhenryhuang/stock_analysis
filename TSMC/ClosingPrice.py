import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_yahoo_finance_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    
    # 確保數據包含必要的欄位
    if 'Close' not in df.columns:
        raise Exception("Failed to fetch Close price data")
    
    return df

start = "2020-01-01"
end = dt.datetime.now().strftime('%Y-%m-%d')

try:
    # 獲取台積電 (2330.TW) 的數據
    df_2330 = get_yahoo_finance_data('2330.TW', start, end)

    # 建立收盤價資料表
    stocks = pd.concat([df_2330['Close']], axis=1, keys=["TSMC"])
    
    # 標示股票價的 10% 到 90% 價格區間 (價格抓月收盤量的平均)
    tsmc_upper = stocks['TSMC'].resample('M').mean().quantile(0.9)
    tsmc_lower = stocks['TSMC'].resample('M').mean().quantile(0.1)
    
    stocks['TSMC'].plot(kind="line", grid=True, figsize=(10, 6), title='TSMC Close Prices')
    plt.hlines([tsmc_upper, tsmc_lower], stocks.index.min(), stocks.index.max(), colors=['red', 'green'], linestyles='dashed')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show()

except Exception as e:
    print(e)
