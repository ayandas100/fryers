import pandas as pd
import numpy as np
from fyers_apiv3 import fyersModel
from datetime import date
today = date.today().strftime("%Y-%m-%d")

def compute_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift(1))
    low_close = np.abs(df['low'] - df['close'].shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def angle(series, atr):
    rad2deg = 180 / np.pi
    slope = rad2deg * np.arctan((series - series.shift(1)) / atr)
    return slope

def main(df):
    df = df
    # Calculate ohlc4
    df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    df['ATR'] = compute_atr(df)

    # EMA20 and its slope
    df['ema20'] = df['ohlc4'].ewm(span=20, adjust=False).mean()
    df['ema20_slope'] = angle(df['ema20'], df['ATR'])

    # Boolean column: is slope >= 4 degrees?
    df['ema20_slope_ge_4'] = df['ema20_slope'] >= 4
    df["timestamp"] = (
        pd.to_datetime(df["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )


    # Print only the final output
    cols_to_show = ['timestamp', 'symbol', 'ema20_slope', 'ema20_slope_ge_4']
    print(df[cols_to_show].dropna().tail(20))  # Show last 10 for brevity

def fryers_hist(symb,fyers):
    # access_token = gen_AcessTok(fyers)
    # fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {"symbol": f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": "2025-07-05", "range_to": today, "cont_flag": "1"}

    candle_data = fyers.history(data)
    return candle_data


if __name__ == '__main__':
    
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2E4OUdrZEJ5YzYtQ3A1UTMweGFmS3Q2dVNJY2FDTXF5bV92WmItWWFYV0gzdk10VmVjT19PODNfdmhCT3RiYVVpMGNSYXZCeWZjdURlSmZ5RFVOVnJ5ZVc0bkpCbXFYZmkySlUzMlJscGx0dkpGTT0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxOTM0NjAwLCJpYXQiOjE3NTE4OTU4NzgsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTg5NTg3OCwic3ViIjoiYWNjZXNzX3Rva2VuIn0.Kt7uQLvrhBYyE-tKfbYnE2h02aSR2FboZ4g0vh-oPJ8"
    symb1 = "NSE:NIFTY2571025350CE"
    symbl2 = "NSE:NIFTY2571025550PE"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")

    candle_data = fryers_hist(symb1,fyers)
    columns_candle = ["timestamp", "open", "high", "low", "close", "volume"]
    
    df_candle = pd.DataFrame(candle_data["candles"],columns=columns_candle)
    df_candle['symbol'] = symb1
    
    man = main(df_candle)
    
    print(man)