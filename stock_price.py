import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf

start = dt.datetime(2024, 1, 1)
end = dt.datetime(2024, 6, 1)

# Fetch data from Yahoo Finance using yfinance
df_2330 = yf.download('2330.TW', start=start, end=end)
df_2454 = yf.download('2454.TW', start=start, end=end)

fig = plt.figure(figsize=(10, 6))
plt.plot(df_2330.Close, label='TSMC')
plt.plot(df_2454.Close, label='MediaTek')
plt.title('TSMC vs MediaTek', loc='center')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True, axis='y')
plt.legend()
plt.show()
mpf.plot(df_2330, type='candle', mav=10, volume=True)