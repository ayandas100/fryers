'''
Created on 11-Jul-2024

@author: User
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download data for Apple
data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Define short-term and long-term windows
short_window = 30
long_window = 100

# Calculate the short-term and long-term moving averages
data['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Create signals
data['signal'] = 0.0
data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1.0, 0.0)
data['positions'] = data['signal'].diff()

# Plot the closing price, short-term, and long-term moving averages
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['short_mavg'], label='30-day SMA')
plt.plot(data['long_mavg'], label='100-day SMA')

# Plot buy signals
plt.plot(data[data['positions'] == 1].index, 
         data['short_mavg'][data['positions'] == 1],
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot sell signals
plt.plot(data[data['positions'] == -1].index, 
         data['short_mavg'][data['positions'] == -1],
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title('Moving Average Crossover Strategy')
plt.legend()
plt.show()

# Calculate returns
data['returns'] = data['Close'].pct_change()

# Calculate strategy returns
data['strategy_returns'] = data['returns'] * data['signal'].shift(1)

# Calculate cumulative returns
data['cumulative_returns'] = (1 + data['returns']).cumprod()
data['cumulative_strategy_returns'] = (1 + data['strategy_returns']).cumprod()

# Plot cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(data['cumulative_returns'], label='Buy and Hold Strategy')
plt.plot(data['cumulative_strategy_returns'], label='Moving Average Crossover Strategy')
plt.title('Cumulative Returns')
plt.legend()
plt.show()