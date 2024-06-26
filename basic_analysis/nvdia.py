import pandas as pd
import datetime as dt
import pandas_datareader.data as data
import matplotlib.pyplot as plt

df = data.DataReader('NVDA', data_source = 'stooq', start='2024-01-01',end='2024-06-01')

# Total weekly trading volume
df['week'] = df.index.isocalendar().week
weekly_volume = df.groupby('week').Volume.sum()
print("Total weekly trading volume : ")
print(weekly_volume)

# Average weekly closing price
weekly_average_close = df.groupby('week').Close.mean()
print("Average weekly closing price : ")
print(weekly_average_close)

# Total monthly transaction volume
df['month'] = df.index.month
monthly_volume = df.groupby('month').Volume.sum()
print("Total monthly transaction volume : ")
print(monthly_volume)

# Daily stock price change percentage
df['price_change_pct'] = df['Close'].pct_change() * 100
print("Daily stock price change percentage : ")
print(df['price_change_pct'])

# 10 day cycle sampling
ten_day_sampling = df.resample('10D').mean()
print("10 day cycle sampling : ")
print(ten_day_sampling)

# Draw stock price trend chart
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Close'], label='Close')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('NVDA')
plt.legend()
plt.grid(True)
plt.show()
