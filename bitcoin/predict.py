import numpy as np
import yfinance as yf
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

def get_yahoo_finance_data(symbol, start, end):
    # 使用 yfinance 下載數據
    df = yf.download(symbol, start=start, end=end)
    
    # 確保數據包含必要的欄位
    if 'Close' not in df.columns:
        raise Exception("Failed to fetch Close price data")
    
    return df

def prepare_data(df, ma_num):
    df['MA'] = df['Close'].rolling(window=ma_num).mean()
    df['Lag1'] = df['Close'].shift(1)
    df['Lag2'] = df['Close'].shift(2)
    df = df.dropna()  # Remove rows with NaN values
    
    features = df[['MA', 'Lag1', 'Lag2']]
    target = df['Close']
    
    return features, target

def train_model(features, target):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('model', GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean-Square Error: {mse}")
    
    return pipeline

def predict_future_prices(df, model, ma_num, predict_days):
    last_index = df.index[-1]
    future_dates = [last_index + dt.timedelta(days=i) for i in range(1, predict_days + 1)]
    
    future_features = df[['MA', 'Lag1', 'Lag2']].iloc[-1:].copy()
    future_features = future_features.fillna(future_features.mean())
    future_prices = []
    
    for date in future_dates:
        predicted_price = model.predict(future_features)[0]
        future_prices.append(predicted_price)
        
        future_features['Lag1'] = predicted_price
        future_features['Lag2'] = future_features['Lag1']
        future_features['MA'] = (df['Close'].iloc[-(ma_num-1):].sum() + predicted_price) / ma_num
    
    future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': future_prices})
    future_df.set_index('Date', inplace=True)
    
    return future_df

#-----------------------#
start = "2020-10-01"
end = dt.datetime.now().strftime('%Y-%m-%d')
predict_days = 30  # 預測未來 30 天

try:
    df_btc = get_yahoo_finance_data('BTC-USD', start, end)
    
    total = 100000  # Initial capital
    stop_earn = 0.1 # Stop profit point 10%
    ma_num = 21     # Moving average window size

    features, target = prepare_data(df_btc, ma_num)
    model = train_model(features, target)
    
    future_df = predict_future_prices(df_btc, model, ma_num, predict_days)
    
    # Plot historical and predicted prices
    plt.figure(figsize=(12, 6))
    plt.plot(df_btc.index, df_btc['Close'], label='Historical Close Prices')
    plt.plot(future_df.index, future_df['Predicted_Close'], label='Predicted Close Prices', linestyle='--')
    plt.title('Bitcoin Historical and Predicted Close Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    
    # 調整 x 軸以包含預測範圍
    all_dates = pd.concat([pd.Series(df_btc.index), pd.Series(future_df.index)])
    plt.xlim(all_dates.min(), all_dates.max())
    
    # 顯示圖表
    plt.show()
    
    print(f"Price After {predict_days} days: {future_df['Predicted_Close'].iloc[-1]}")

except Exception as e:
    print(e)
