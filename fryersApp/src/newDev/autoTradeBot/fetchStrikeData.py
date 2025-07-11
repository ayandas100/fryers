'''
Created on 29-Jun-2025

@author: User
'''
'''
Created on 13-Apr-2024

@author: User
'''
from datetime import date
# from fyers_api import fyersModel
# from fyers_api import accessToken
import os
from fyers_apiv3 import fyersModel
import datetime as dt
import json
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
import duckdb as db
import pandas_ta as ta
from placeOrder import check_order_status,place_bo_order,get_order_state
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import numpy as np
from highlight_row import highlight_supertrend
from ta.momentum import RSIIndicator
import ta
import time

client_id = "15YI17TORX-100"
today = date.today().strftime("%Y-%m-%d")
yesterday = datetime.today() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')


def getAuthCode():
    client_id = "15YI17TORX-100"
    secret_key = "2HJ9AD57A5"
    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
    response_type = "code"  
    state = "sample_state"
    grant_type = "authorization_code"  

    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type,
        grant_type=grant_type
        
    )

    # Generate the auth code using the session model
    auth_codeURL = session.generate_authcode()
    return auth_codeURL

access_token = None
def gen_AcessTok(auth_code):
    global access_token
    if access_token is None:
        secret_key = "2HJ9AD57A5"
        redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
        response_type = "code"  
        state = "sample_state"
        grant_type = "authorization_code"  

        # Create a session model with the provided credentials
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type=response_type,
            grant_type=grant_type
            
        )

        # Generate the auth code using the session model
        auth_codeURL = session.generate_authcode()
        print(auth_codeURL)
        auth_code=auth_code
        # Set the authorization code in the session object
        session.set_token(auth_code)

        # Generate the access token using the authorization code
        access_token = session.generate_token()["access_token"]
    return access_token



def fryers_hist(symb,auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {"symbol":f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": yesterday, "range_to": today, "cont_flag": "1"}

    candle_data = fyers.history(data)
    return candle_data

def fryers_chain(auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {
        "symbol":"NSE:NIFTY50-INDEX",
        "strikecount":30,
        
    }
    response = fyers.optionchain(data=data)
    return response

## for ordering block
def fryersOrder(auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
    return fyers

# def compute_atr(df, period=14):
#     high_low = df['high'] - df['low']
#     high_close = np.abs(df['high'] - df['close'].shift(1))
#     low_close = np.abs(df['low'] - df['close'].shift(1))
#     tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
#     atr = tr.rolling(window=period).mean()
#     return atr

def angle(series, atr):
    rad2deg = 180 / np.pi
    slope = rad2deg * np.arctan((series - series.shift(1)) / atr)
    return slope

def maAngle(df):
    df = df
    # Calculate ohlc4
    df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    # df['ATR1'] = compute_atr(df)

    # EMA20 and its slope
    df['ema20'] = df['ohlc4'].ewm(span=20, adjust=False).mean()
    df['ema20_slope'] = angle(df['ema20'], df['ATR'])



    # Boolean column: is slope >= 4 degrees?
    df['ma20 SL4'] = df['ema20_slope'] >= 4
    
    return df

from ta.momentum import RSIIndicator

def compute_rsi(df, price_col='close', period=14, smoothing_period=14):
    df = df.copy()
    
    # Compute RSI using Wilder’s method (ta lib matches TradingView)
    rsi_calc = RSIIndicator(close=df[price_col], window=period)
    df['RSI'] = rsi_calc.rsi()
    
    # Add arrow column showing RSI rising
    arrow = '\u2191'
    df[f'RSI {arrow}'] = df['RSI'] > df['RSI'].shift(1)
    df['RSI_Smooth'] = df['RSI'].rolling(window=smoothing_period).mean()
    df[f'RSI{arrow} SML'] = df['RSI'] > df['RSI_Smooth']
    
    return df

def compute_atr(df, period=14):
    df = df.copy()
    atr_indicator = ta.volatility.AverageTrueRange(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=period,
        fillna=False
    )
    df['ATR'] = atr_indicator.average_true_range()
    return df

def compute_cvd(df, close_col='close', volume_col='volume'):
    df = df.copy()
    
    # Calculate price change
    close_diff = df[close_col].diff()

    # Estimate delta (buy vs sell volume)
    df['delta'] = np.where(
        close_diff > 0, df[volume_col], 
        np.where(close_diff < 0, -df[volume_col], 0)
    )
    
    # Cumulative Volume Delta
    df['CVD'] = df['delta'].cumsum()
    
    # CVD Up Arrow: is CVD increasing?
    arrow = '\u2191'  # ↑
    df[f'CVD {arrow}'] = df['CVD'] > df['CVD'].shift(1)
    
    return df

def detect_ema9_bounce(df):
    df = df.copy()

    # Step 1: Calculate EMA9
    df['EMA9'] = df['close'].ewm(span=9, adjust=False).mean()

    # Step 2: Shifted values for comparison
    df['prev_close'] = df['close'].shift(1)
    df['prev_low'] = df['low'].shift(1)
    df['prev_ema9'] = df['EMA9'].shift(1)

    # Step 3: Bounce Condition
    df['EMA9_support_bounce_base'] = (
        (df['prev_low'] <= df['prev_ema9']) &           # previous low dipped to or below EMA9
        (df['prev_close'] > df['prev_ema9']) &          # previous close above EMA9
        (df['close'] > df['open']) &                    # current candle is green
        (df['close'] > df['EMA9'])                      # current close above EMA9
    )

    # Step 4: Fresh Bounce — no bounce in previous candle
    df['EMA9 SuP'] = df['EMA9_support_bounce_base'] & \
                     (~df['EMA9_support_bounce_base'].shift(1).fillna(True))

    return df

from tabulate import tabulate

def print_bool_fields(df):
    """
    Print all columns from the latest row (most recent candle) in key=value format.
    """
    latest_row = df.iloc[0]  # Most recent row (assuming df is sorted descending by time)
    output = " | ".join(f"{col}={latest_row[col]}" for col in df.columns)
    print(f"{output}")



# the logic block
def start_bot(symb,auth_code):
    
    resp =  fryers_chain(auth_code)
    # resp =  auth_code
    # print(resp)
    df_op = pd.DataFrame(resp["data"]["optionsChain"])
    columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]
    df_op = df_op[columns]
    
    ### read the data for selected strike price
    #NSE:NIFTY2570325600CE 
    ### read the data for selected strike price
    #NSE:NIFTY2570325600CE 
    
    candle_data = fryers_hist(symb,auth_code)
    columns_candle = ["timestamp", "open", "high", "low", "close", "volume"]
    df_candle = pd.DataFrame(candle_data["candles"],columns=columns_candle)
   
    df_candle["timestamp"] = (
        pd.to_datetime(df_candle["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
        .dt.strftime("%m-%d %H:%M")
    )

    df_candle = df_candle.sort_values(by="timestamp").reset_index(drop=True)
    df_candle.ta.supertrend(length=11, multiplier=2.0, append=True)
    df_candle.ta.supertrend(length=10, multiplier=1.0, append=True)
    df_candle["symbol"] = symb
   
    df_candle = df_candle[['symbol','timestamp','open','close','SUPERT_11_2.0','SUPERT_10_1.0','high','low','volume']].rename(columns={'SUPERT_11_2.0':'supertrend','SUPERT_10_1.0':'supertrend10'})
    df_candle = df_candle.drop_duplicates(subset='timestamp', keep='first')

    df_candle.loc[:, 'MA20'] = df_candle['close'].rolling(window=20).mean()
    df_candle.loc[:,'Above_MA20'] = df_candle['close'] > df_candle['MA20']
    df_candle.loc[:, 'prev_Above_MA20'] = df_candle['Above_MA20'].shift(1)
    df_candle.loc[:,'20 CXover'] = (df_candle['Above_MA20'] == True) & (df_candle['prev_Above_MA20'] == False)
    df_candle.loc[:,'Above ST11'] = df_candle['close'] > df_candle['supertrend']
    df_candle.loc[:,'Above ST10'] = df_candle['close'] > df_candle['supertrend10']
    # #ATR calculations
    df_candle = compute_atr(df_candle)
    arrow = '\u2191'
    df_candle[f'ATR {arrow}'] = df_candle['ATR'] > df_candle['ATR'].shift(1)
    # MA 20 Bounce calculation
    # arrow = '\u2191'
    df_candle['prev_close'] = df_candle['close'].shift(1)
    df_candle['prev_low'] = df_candle['low'].shift(1)
    df_candle['prev_ma20'] = df_candle['MA20'].shift(1)
    df_candle['MA20_support_bounce_base'] = ((df_candle['prev_low'] <= df_candle['prev_ma20']) & (df_candle['prev_close'] > df_candle['prev_ma20']) &  (df_candle['close'] > df_candle['open']) & (df_candle['close'] > df_candle['MA20']))
    df_candle['MA20 SuP'] = df_candle['MA20_support_bounce_base'] & \
                        (~df_candle['MA20_support_bounce_base'].shift(1).fillna(True))
                        # (~df_candle['20 CXover']) & \
                        # (~df_candle['20 CXover'].shift(1).fillna(False))

    df_candle = maAngle(df_candle)
    df_candle = compute_rsi(df_candle)
    df_candle = compute_cvd(df_candle)
    df_candle = detect_ema9_bounce(df_candle)
   
    dbdf = db.query("select a.*,b.ltp " \
"               from df_candle a" \
"               join df_op b" \
"               on a.symbol=b.symbol")
    df = dbdf.df()
    df[f'LTP {arrow}'] = df['ltp'] > df['high'].shift(1)
    df[f'EMA{arrow} MA'] = df['EMA9'] > df['MA20']
    # df = df.set_index('timestamp')
    df = df[['timestamp','high','close','ltp','supertrend10','supertrend','20 CXover','MA20 SuP','EMA9 SuP',f'EMA{arrow} MA',f'LTP {arrow}','Above ST11','Above ST10',f'ATR {arrow}',f'CVD {arrow}','ma20 SL4',f'RSI {arrow}',f'RSI{arrow} SML','ATR','RSI']]. \
                rename(columns={'ltp':'LTP','timestamp':'Time','supertrend':'ST 11','supertrend10':'ST 10','20 CXover':'20 CXvr','ATR':'ATR','Above ST11':f'ST11{arrow}','Above ST10':f'ST10{arrow}'})
    # df = df.reset_index(drop=True)
    # df.index.name = None
    df = df.sort_values(by='Time', ascending=False)
    df = df.head(35)


    fyers = fryersOrder(auth_code)
    get_order_state()
    check_order_status(fyers)

    latest = df.iloc[0]
    previous = df.iloc[1]

    ### entry conditions
    entry_trigger = (previous['20 CXvr'] or previous['MA20 SuP'] or latest['20 CXvr'] or latest['MA20 SuP'] or previous['EMA9 SuP']) and latest[f'ST11{arrow}'] and latest[f'ST10{arrow}'] and latest[f'LTP {arrow}'] and latest[f'CVD {arrow}']
    first_block = latest['ATR'] >= 8.40 and latest[f'ATR {arrow}'] and latest['ma20 SL4'] and latest[f'RSI {arrow}'] and previous[f'RSI{arrow} SML'] and latest[f'RSI{arrow} SML'] and latest[f'EMA{arrow} MA'] and previous[f'EMA{arrow} MA']
    second_block = latest['RSI'] >= 63 and latest[f'RSI {arrow}'] and latest[f'ATR {arrow}'] and latest[f'RSI{arrow} SML'] and latest[f'EMA{arrow} MA'] and  previous[f'RSI{arrow} SML']
    third_block = latest[f'ST11{arrow}'] and latest[f'ST10{arrow}'] and latest['RSI'] >= 70 and previous['RSI'] >= 68 and latest[f'RSI {arrow}'] and latest[f'ATR {arrow}'] and latest['ATR'] >= 12 and latest[f'LTP {arrow}'] and latest[f'CVD {arrow}'] and latest[f'RSI{arrow} SML'] and latest[f'EMA{arrow} MA'] and previous[f'EMA{arrow} MA']
    
   
  
    if (entry_trigger and first_block) or (entry_trigger and second_block) or third_block :

        stop_loss = 8
        target = 10
        qty = 75
        symbol = symb
        
        order_response = place_bo_order(fyers, symbol, qty, stop_loss, target)
        if order_response.get("message") == "Successfully placed order":
            time.sleep(3)
    else:
        order_response = {
            "message": "Conditions not met for placing order."
        }

    
    styled_html = df.style.apply(highlight_supertrend, axis=1).format(precision=2)\
                    .set_table_styles(
                        [{'selector': 'td', 'props': [('white-space', 'normal'), ('word-wrap', 'break-word')]},
                        {'selector': 'th', 'props': [('white-space', 'normal'), ('word-wrap', 'break-word')]}]
                    )\
                    .to_html(table_attributes='class="table table-bordered table-hover table-sm w-100"')

    
    return styled_html,order_response.get("message"),df





