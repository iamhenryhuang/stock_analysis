import requests
import pandas as pd
import datetime as dt
import time
import io
import matplotlib.pyplot as plt
import mplfinance as mpf

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
    
    # Parse the CSV data using io.StringIO
    data = response.content.decode('utf-8')
    df = pd.read_csv(io.StringIO(data))
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    return df

start = dt.datetime(2024, 1, 1)
end = dt.datetime(2024, 6, 1)

try:
    time.sleep(5)
    df_2330 = get_yahoo_finance_data('2330.TW', start, end)
    df_2454 = get_yahoo_finance_data('2454.TW', start, end)
    
    fig = plt.figure(figsize=(10, 6))
    plt.plot(df_2330.Close, label='TSMC')
    plt.plot(df_2454.Close, label='MediaTek')
    plt.title('TSMC vs MediaTek', loc='center')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True, axis='y')
    plt.legend()
    plt.show()

    # draw k line
    mpf.plot(df_2330, type='candle', mav=10, volume=True)
    #df_2330.to_excel('stock_price.xlsx', index=False, engine='openpyxl')

except Exception as e:
    print(f"An error occurred: {e}")
