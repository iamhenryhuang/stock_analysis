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

def strategy(df, total, ma_num, stop_earn):
    df['MA'] = df['Close'].rolling(window=ma_num).mean()
    state = 'wait_long'
    entry_price = 0
    shares = 0
    better_buy = None
    better_sell = None
    better_profit = 0

    for i in range(len(df)):
        close = df['Close'].iloc[i]
        ma = df['MA'].iloc[i]
        
        if state == 'wait_long':
            if close > ma:
                state = 'enter_long'
                entry_price = close
                shares = total / close
                total = 0
                buy_date = df.index[i].date()
                print(f"Enter long at {buy_date} with price {entry_price}")
        elif state == 'enter_long':
            if close < ma or close >= entry_price * (1 + stop_earn):
                state = 'wait_short'
                total = shares * close
                shares = 0
                sell_date = df.index[i].date()
                profit = total - 100000  # 假設初始資金是 100000
                print(f"Exit long at {sell_date} with price {close} and profit {profit}")
                if profit > better_profit:
                    better_profit = profit
                    better_buy = (buy_date, entry_price)
                    better_sell = (sell_date, close)

    # Calculate final value if still in a position
    if shares > 0:
        total = shares * df['Close'].iloc[-1]
        sell_date = df.index[-1].date()
        profit = total - 100000  # 假設初始資金是 100000
        if profit > better_profit:
            better_profit = profit
            better_buy = (buy_date, entry_price)
            better_sell = (sell_date, df['Close'].iloc[-1])

    print(f"Better Buy Point: {better_buy}")
    print(f"Better Sell Point: {better_sell}")

    return better_buy, better_sell


#-----------------------#
start = dt.datetime(2024, 5, 1)
end = dt.datetime.now()

try:
    time.sleep(5)

    df_btc = get_yahoo_finance_data('BTC-USD', start, end)
    
    total = 100000  # 初始資金
    ma_num = 21     # 移動平均窗口大小
    stop_earn = 0.1 # 停利點 10%

    better_buy, better_sell = strategy(df_btc, total, ma_num, stop_earn)
    
    # 繪製 價格 & 均線圖
    df_btc['MA'] = df_btc['Close'].rolling(window=ma_num).mean()
    selected_data = df_btc.loc['2024-06-07':'2024-07-07', ['Close', 'MA']]
    
    selected_data.plot(kind='line', grid=True, figsize=(10, 10), title='Bitcoin Close Prices and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(['Close Price', '21-Day MA'])
    plt.subplots_adjust(bottom=0.2)
    plt.show()

except Exception as e:
    print(e)

# note
"""
當收盤價從等於均價後，漸漸大於均價 -> 買點 可以做多
當收盤價漸漸下跌，且準備等於均價 -> 賣點 可以做空
"""
