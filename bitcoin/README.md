# Bitcoin Trading Strategy Backtesting

This project implements a simple moving average crossover strategy to backtest Bitcoin trading using historical data from Yahoo Finance.

## Overview

The strategy involves using the 21-day moving average to determine buy and sell signals:
- **Buy Signal**: When the closing price crosses above the 21-day moving average.
- **Sell Signal**: When the closing price crosses below the 21-day moving average or exceeds the entry price by a predefined percentage (stop-earn).

## Features

- Fetch historical Bitcoin data from Yahoo Finance.
- Implement a trading strategy based on moving average crossover.
- Calculate and display the best buy and sell points.
- Plot the historical closing prices and moving averages.

## Requirements

- Python 3.x
- `requests`
- `pandas`
- `matplotlib`

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/bitcoin-trading-strategy.git
    cd bitcoin-trading-strategy
    ```

2. Install the required packages:
    ```bash
    pip install requests pandas matplotlib
    ```

## Usage

1. Run the backtesting script:
    ```bash
    python backtest.py
    ```

2. The script fetches Bitcoin data from Yahoo Finance, applies the trading strategy, and plots the results.

## Code Explanation

### Data Fetching

The `get_yahoo_finance_data` function fetches historical data for Bitcoin from Yahoo Finance:

```python
def get_yahoo_finance_data(symbol, start, end):
    ...
