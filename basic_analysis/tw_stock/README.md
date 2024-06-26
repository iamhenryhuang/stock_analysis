# Stock Price Visualization for TSMC and MediaTek

## Overview
This repository contains a Python script that fetches and visualizes the stock price data for TSMC (2330.TW) and MediaTek (2454.TW) using Yahoo Finance. The data covers the period from May 1, 2024, to June 26, 2024. This visualization helps in comparing the closing stock prices of these two prominent Taiwanese semiconductor companies over the specified period.

## Dependencies
The script uses several Python packages to handle data fetching, processing, and visualization:

- `yfinance`: Used for downloading historical market data from Yahoo Finance.
- `matplotlib`: Utilized for creating static, interactive, and animated visualizations in Python. This project specifically uses `matplotlib` for plotting the closing prices of the stocks.

### Special Note on mplfinance
While this project currently does not use `mplfinance` directly, it is an excellent library for financial data visualization and could be integrated for more advanced financial plots. More information about mplfinance can be found on its GitHub page: [mplfinance GitHub](https://github.com/matplotlib/mplfinance)

## Usage
To run the script, ensure that you have the required packages installed. You can install the dependencies using pip:
```bash
pip install yfinance matplotlib
