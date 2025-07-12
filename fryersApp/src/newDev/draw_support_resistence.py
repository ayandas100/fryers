from datetime import date
from fyers_api import fyersModel
from fyers_api import accessToken
import os
from fyers_apiv3 import fyersModel
import datetime as dt
import json
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
import duckdb as db
import pandas_ta as ta
# from autoTradeBot.placeOrder import check_order_status,place_bo_order
from autoTradeBot.symbolLoad import loadSymbol
import numpy as np
import ta
from datetime import datetime, timedelta


today = date.today().strftime("%Y-%m-%d")
yesterday = datetime.today() - timedelta(days=10)
yesterday = yesterday.strftime('%Y-%m-%d')


def fryers_hist(symb,fyers):
    # access_token = gen_AcessTok(fyers)
    # fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {"symbol": f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": yesterday, "range_to": today, "cont_flag": "1"}

    candle_data = fyers.history(data)
    return candle_data

def fryers_chain(fyers):
    # access_token = gen_AcessTok(auth_code)
    # fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {
        "symbol":"NSE:NIFTY50-INDEX",
        "strikecount":30,
        
    }
    response = fyers.optionchain(data=data)
    return response


def detect_pivots(df, period=10):
    df = df.copy()
    df['pivot_high'] = df['high'].rolling(window=2 * period + 1, center=True).apply(
        lambda x: int(x[period] == max(x)), raw=True
    ).fillna(0).astype(bool)
    
    df['pivot_low'] = df['low'].rolling(window=2 * period + 1, center=True).apply(
        lambda x: int(x[period] == min(x)), raw=True
    ).fillna(0).astype(bool)
    
    return df

def find_sr_zones(df, channel_width_pct=5, loopback=290, min_strength=2, max_zones=10):
    df = df.reset_index(drop=True)
    pivot_vals = []
    pivot_types = []

    for i in range(len(df)):
        if df.loc[i, 'pivot_high']:
            pivot_vals.append(df.loc[i, 'high'])
            pivot_types.append('high')
        elif df.loc[i, 'pivot_low']:
            pivot_vals.append(df.loc[i, 'low'])
            pivot_types.append('low')

    zones = []

    for i in range(len(pivot_vals)):
        ref_val = pivot_vals[i]
        zone_min = ref_val - (ref_val * channel_width_pct / 100)
        zone_max = ref_val + (ref_val * channel_width_pct / 100)
        strength = sum(zone_min <= pv <= zone_max for pv in pivot_vals)
        if strength >= min_strength:
            zones.append((zone_min, zone_max, strength))

    strong_zones = sorted(zones, key=lambda x: x[2], reverse=True)
    final_zones = []
    seen = []

    for zone in strong_zones:
        midpoint = (zone[0] + zone[1]) / 2
        if all(abs(midpoint - (z[0] + z[1]) / 2) > (midpoint * channel_width_pct / 100) for z in seen):
            seen.append(zone)
            final_zones.append(zone)
        if len(final_zones) >= max_zones:
            break

    # Add symbol from original df (assumes same symbol in all rows)
    symbol = df['symbol'].iloc[0] #if 'symbol' in df.columns else 'N/A'

    zone_df = pd.DataFrame(final_zones, columns=['zone_low', 'zone_high', 'strength'])
    zone_df['type'] = np.where((zone_df['zone_low'] + zone_df['zone_high']) / 2 > df['close'].iloc[-1], 'resistance', 'support')
    zone_df['label'] = np.where(zone_df['strength'] >= 5, 'strong', 'weak')
    zone_df['symbol'] = symbol

    return zone_df.sort_values(by='zone_low').reset_index(drop=True)


def extract_strong_resistance_with_original_range(zones_df):
    """
    Return only one strong resistance zone with its original zone_low and zone_high.
    """
    symbol = zones_df['symbol'].iloc[0] if 'symbol' in zones_df.columns else 'N/A'

    resistance_zones = zones_df[
        (zones_df['type'] == 'resistance') & (zones_df['label'] == 'strong')
    ]

    if not resistance_zones.empty:
        resistance_zone = resistance_zones.loc[resistance_zones['zone_low'].idxmin()]
        return pd.DataFrame([{
            'symbol': symbol,
            'Rlow': resistance_zone['zone_low'],
            'Rhigh': resistance_zone['zone_high'],
            'type': 'resistance'
        }])

    return pd.DataFrame()  # Return empty if no strong resistance found


def start_bot(symb,fyers):
    
    resp =  fryers_chain(fyers)
    # resp =  auth_code
    # print(resp)
    df_op = pd.DataFrame(resp["data"]["optionsChain"])
    columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]
    df_op = df_op[columns]
    
    ### read the data for selected strike price
    #NSE:NIFTY2570325600CE 
    ### read the data for selected strike price
    #NSE:NIFTY2570325600CE 
    
    candle_data = fryers_hist(symb,fyers)
    columns_candle = ["timestamp", "open", "high", "low", "close", "volume"]
    df_candle = pd.DataFrame(candle_data["candles"],columns=columns_candle)
    df_candle["symbol"] = symb
   
    df_candle["timestamp"] = (
        pd.to_datetime(df_candle["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    df = detect_pivots(df_candle, period=10)
    zones = find_sr_zones(df)
    df = extract_strong_resistance_with_original_range(zones)

    return print(df_candle.head(5))




if __name__ == '__main__':
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2NnbVltTzVISTJWX3E5QTRGMkt6QmVnY013cXBJV01JX2JQc3I1WXdBTXNXdkdIeVRFUXlHVFdBTk1GZFFvMGhma0JudENhY0ktRmcwdXZFQzBTUVpTLWZEZVFlSm05TFRUV2EzdmxJT01Dd000RT0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUyMzY2NjAwLCJpYXQiOjE3NTIzMDQwMjQsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MjMwNDAyNCwic3ViIjoiYWNjZXNzX3Rva2VuIn0.Ut7_ir7i53hI5oNdy6tm69MlEeFw2JFMyB9gMsyEJkM"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")
    symb1 = "NSE:NIFTY2571725250PE"
    ce = start_bot(symb1,fyers)
    print(ce)
