import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fyers_apiv3 import fyersModel


client_id = "15YI17TORX-100"
# Step 1: Simulate OHLC data (Replace with actual trading data if available)
def main():
    np.random.seed(42)
    n = 300
    dates = pd.date_range('2023-01-01', periods=n, freq='D')
    price = np.cumsum(np.random.randn(n)) + 100
    ohlc = pd.DataFrame({
        'date': dates,
        'open': price + np.random.randn(n),
        'high': price + np.random.rand(n) * 2,
        'low': price - np.random.rand(n) * 2,
        'close': price + np.random.randn(n)
    })
    ohlc.set_index('date', inplace=True)

    # Step 2: ohlc4 = average of OHLC
    ohlc['ohlc4'] = (ohlc['open'] + ohlc['high'] + ohlc['low'] + ohlc['close']) / 4

    # Step 3: Compute ATR
    def compute_atr(df, period=14):
        high, low, close = df['high'], df['low'], df['close']
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

    ohlc['ATR'] = compute_atr(ohlc)

    # Step 4: JMA function
    def jma(src, length, phase, power):
        phase_ratio = 0.5 if phase < -100 else 2.5 if phase > 100 else phase / 100 + 1.5
        beta = 0.45 * (length - 1) / (0.45 * (length - 1) + 2)
        alpha = beta ** power
        jma_vals = []
        e0_prev, e1_prev, e2_prev, jma_prev = 0, 0, 0, 0

        for i in range(len(src)):
            x = src.iloc[i]
            e0 = (1 - alpha) * x + alpha * e0_prev
            e1 = (x - e0) * (1 - beta) + beta * e1_prev
            e2 = (e0 + phase_ratio * e1 - jma_prev) * (1 - alpha)**2 + (alpha**2) * e2_prev
            jma_val = e2 + jma_prev

            jma_vals.append(jma_val)
            e0_prev, e1_prev, e2_prev, jma_prev = e0, e1, e2, jma_val

        return pd.Series(jma_vals, index=src.index)

    # Step 5: Calculate MAs
    ohlc['jma'] = jma(ohlc['ohlc4'], 10, 50, 1)
    ohlc['jma_fast'] = jma(ohlc['ohlc4'], 10, 50, 2)
    ohlc['ema20'] = ohlc['ohlc4'].ewm(span=20, adjust=False).mean()
    ohlc['ema50'] = ohlc['ohlc4'].ewm(span=50, adjust=False).mean()
    ohlc['ema278'] = ohlc['ohlc4'].ewm(span=278, adjust=False).mean()

    # Step 6: Compute slope angles in degrees
    def angle(series, atr):
        delta = series.diff()
        rad2deg = 180 / np.pi
        slope_angle = rad2deg * (delta / atr)
        return slope_angle

    ohlc['jma_slope'] = angle(ohlc['jma'], ohlc['ATR'])
    ohlc['jma_fast_slope'] = angle(ohlc['jma_fast'], ohlc['ATR'])
    ohlc['ema20_slope'] = angle(ohlc['ema20'], ohlc['ATR'])
    ohlc['ema50_slope'] = angle(ohlc['ema50'], ohlc['ATR'])
    ohlc['ema278_slope'] = angle(ohlc['ema278'], ohlc['ATR'])

    # Step 7: Plot sample slope lines
    ohlc[['ema20_slope']].plot(
        figsize=(14, 6), title='Moving Average Slope Angles (in Degrees)'
    )
    plt.axhline(0, color='black', linestyle='--', alpha=0.6)
    plt.ylabel("Angle (Degrees)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2EwTjdES1JuNEJRbkt2bDZSWk1vd2JoWkY0VG14R2xvWnI4LWdBSWg4bElIVnlzYnFzNWVka3pKQmpON0VRT2J5dGhkb1lGekg1VmJ1OFJWNWQ3STkxSnpjWGtjRThPWVNDNmJsWTlQZ0YxbkcyYz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxOTM0NjAwLCJpYXQiOjE3NTE4NjAwOTEsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTg2MDA5MSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.KKxoZsjxfaU5C5NzcgInn-WAIzMBmavcIRp_IKfhQoE"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")
    symb1 = "NSE:NIFTY2571025450CE"
    symbl2 = "NSE:NIFTY2571025550PE"