import requests
import pandas as pd
import datetime as dt
import time
import io
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf

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

def calculate_roi(df):
    initial_price = df['Close'].iloc[0]
    final_price = df['Close'].iloc[-1]
    roi = ((final_price - initial_price) / initial_price) * 100
    return roi

def plot_closing_prices(df, symbol):
    figure = plt.figure(figsize=(10, 6))
    plt.plot(df.Close, label=symbol)
    plt.title(symbol, loc='center')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True, axis='y')
    plt.legend()
    plt.show()

def plot_candlestick_chart(df):
    mpf.plot(df, type='candle', mav=10, volume=True)

def save_to_excel(df, filename):
    df.to_excel(filename, index=False, engine='openpyxl')

def add_week_and_month_columns(df):
    df['week'] = df.index.isocalendar().week
    df['month'] = df.index.month

def calculate_weekly_average_close(df):
    return df.groupby('week').Close.mean()

def calculate_monthly_volume(df):
    return df.groupby('month').Volume.sum()

def calculate_daily_price_change_percentage(df):
    df['price_change_pct'] = df['Close'].pct_change() * 100
    return df['price_change_pct']

def calculate_ten_day_sampling(df):
    return df.resample('10D').mean()

# Main execution
start = dt.datetime(2024, 1, 1)
end = dt.datetime(2024, 7, 1)
symbol = '0050.TW'
filename = 'etf.xlsx'

time.sleep(5)
df_0050 = get_yahoo_finance_data(symbol, start, end)

plot_closing_prices(df_0050, symbol)
plot_candlestick_chart(df_0050)
save_to_excel(df_0050, filename)
add_week_and_month_columns(df_0050)

weekly_average_close = calculate_weekly_average_close(df_0050)
print("Average weekly closing price : ")
print(weekly_average_close)
print("=====================================")

monthly_volume = calculate_monthly_volume(df_0050)
print("Total monthly transaction volume : ")
print(monthly_volume)
print("=====================================")

daily_price_change_pct = calculate_daily_price_change_percentage(df_0050)
print("Daily stock price change percentage : ")
print(daily_price_change_pct)
print("=====================================")

ten_day_sampling = calculate_ten_day_sampling(df_0050)
print("10 day cycle sampling : ")
print(ten_day_sampling)
print("=====================================")

roi = calculate_roi(df_0050)
print(f"Investment Return (ROI): {roi:.2f}%")
