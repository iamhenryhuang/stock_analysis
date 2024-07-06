import numpy as np
import sklearn.linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
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
    
    data = response.content.decode('utf-8')
    df = pd.read_csv(io.StringIO(data))
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    return df

def prepare_data(df, ma_num):
    df['MA'] = df['Close'].rolling(window=ma_num).mean()
    df['Lag1'] = df['Close'].shift(1)
    df['Lag2'] = df['Close'].shift(2)
    df = df.dropna()  # 刪除含有 NaN 值的行
    
    features = df[['MA', 'Lag1', 'Lag2']]
    target = df['Close']
    
    return features, target

def train_polynomial_model(features, target, degree=3):
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(features)
    X_train, X_test, y_train, y_test = train_test_split(X_poly, target, test_size=0.2, random_state=42)
    model = sklearn.linear_model.LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    #print(f"Mean-Square Error: {mse}")
    
    return model, poly

def predict_future_prices(df, model, poly, ma_num, predict_days):
    last_index = df.index[-1]
    future_dates = [last_index + dt.timedelta(days=i) for i in range(1, predict_days + 1)]
    
    future_features = df[['MA', 'Lag1', 'Lag2']].iloc[-1:].copy()
    future_prices = []
    
    for date in future_dates:
        future_features_poly = poly.transform(future_features)
        predicted_price = model.predict(future_features_poly)[0]
        future_prices.append(predicted_price)
        
        future_features['Lag1'] = predicted_price
        future_features['Lag2'] = future_features['Lag1']
        future_features['MA'] = (df['Close'].iloc[-(ma_num-1):].sum() + predicted_price) / ma_num
    
    future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': future_prices})
    future_df.set_index('Date', inplace=True)
    
    return future_df

#-----------------------#
start = dt.datetime(2020, 10, 1)
end = dt.datetime.now()
predict_days = 1

try:
    time.sleep(5)

    df_btc = get_yahoo_finance_data('BTC-USD', start, end)
    
    ma_num = 21     # 移動平均窗口大小

    features, target = prepare_data(df_btc, ma_num)
    model, poly = train_polynomial_model(features, target, degree=3)
    
    future_df = predict_future_prices(df_btc, model, poly, ma_num, predict_days)
    
    # 繪製價格 & 預測價格圖
    plt.figure(figsize=(12, 6))
    plt.plot(df_btc.index, df_btc['Close'], label='Historical Close Prices')
    plt.plot(future_df.index, future_df['Predicted_Close'], label='Predicted Close Prices', linestyle='--')
    plt.title('Bitcoin Historical and Predicted Close Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Price After {predict_days} day: {future_df['Predicted_Close'].iloc[-1]}")

except Exception as e:
    print(e)
