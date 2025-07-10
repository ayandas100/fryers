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



client_id = "15YI17TORX-100"
# secret_key = "2HJ9AD57A5"
# redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
# response_type = "code"  
# state = "sample_state"
# grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")
symbol_list = []

# access_token = None
# def gen_AcessTok(auth_code):
#     global access_token
#     if access_token is None:
#         secret_key = "2HJ9AD57A5"
#         redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
#         response_type = "code"  
#         state = "sample_state"
#         grant_type = "authorization_code"  

#         # Create a session model with the provided credentials
#         session = fyersModel.SessionModel(
#             client_id=client_id,
#             secret_key=secret_key,
#             redirect_uri=redirect_uri,
#             response_type=response_type,
#             grant_type=grant_type
            
#         )

#         # Generate the auth code using the session model
#         auth_codeURL = session.generate_authcode()
#         print(auth_codeURL)
#         auth_code=auth_code
#         # Set the authorization code in the session object
#         session.set_token(auth_code)

#         # Generate the access token using the authorization code
#         access_token = session.generate_token()["access_token"]
#     return access_token

# symb_optionchain="NSE:NIFTY50-INDEX"


def highlight_supertrend(row):
    supertrend = row['supertrend']
    close = row['close']
    
    if pd.isna(supertrend) or pd.isna(close):
        return [''] * len(row)

    styles = [''] * len(row)
    
    # Get column index of 'supertrend'
    st_index = row.index.get_loc('supertrend')

    if supertrend < close:
        styles[st_index] = 'background-color: lightgreen'
    elif supertrend > close:
        styles[st_index] = 'background-color: lightcoral'

    return styles

# def calculate_atr(df, period=14):
#     df['H-L'] = df['High'] - df['Low']
#     df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
#     df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))

#     df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
#     df['ATR'] = df['TR'].rolling(window=period).mean()

#     return df[['High', 'Low', 'Close', 'ATR']]

def fryers_hist(symb,fyers):
    # access_token = gen_AcessTok(fyers)
    # fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {"symbol": f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": "2025-06-26", "range_to": today, "cont_flag": "1"}

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


# def fryersOrder(auth_code):
#     access_token = gen_AcessTok(auth_code)
#     fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
#     return fyers


# def selectStrike(df):
#     if not symbol_list:
#         dfd_ce = db.query("select max(symbol) as ce_sm from df where ltp >= 150 and ltp <=200 and option_type = 'CE'").df()
#         ce = dfd_ce.iloc[0, 0]
#         symbol_list.append(ce)
#         dfd_pe = db.query("select max(symbol) as pe_sm from df where ltp >= 150 and ltp <=200 and option_type = 'PE'").df()
#         pe = dfd_pe.iloc[0, 0]
#         symbol_list.append(pe)
#         return symbol_list


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
    df['ma20SL_ge4'] = df['ema20_slope'] >= 4

    return df

def compute_rsi(df, price_col='close', period=14):
    df = df.copy()
    delta = df[price_col].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    arrow = '\u2191'
    df[f'RSI {arrow}'] = df['RSI'] > df['RSI'].shift(1)
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
   
    df_candle["timestamp"] = (
        pd.to_datetime(df_candle["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
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
    df_candle['prev_close'] = df_candle['close'].shift(1)
    df_candle['prev_low'] = df_candle['low'].shift(1)
    df_candle['prev_ma20'] = df_candle['MA20'].shift(1)
    df_candle['MA20_support_bounce_base'] = ((df_candle['prev_low'] <= df_candle['prev_ma20']) & (df_candle['prev_close'] > df_candle['prev_ma20']) &  (df_candle['close'] > df_candle['open']) & (df_candle['close'] > df_candle['MA20']))
    df_candle['MA20 SuP'] = (df_candle['MA20_support_bounce_base'] & (~df_candle['MA20_support_bounce_base'].shift(1).fillna(False)))
    # df = df_candle                         
    df_candle = maAngle(df_candle)
    df_candle = compute_rsi(df_candle)
    df_candle = compute_cvd(df_candle)

    dbdf = db.query("select a.*,b.ltp " \
"               from df_candle a" \
"               join df_op b" \
"               on a.symbol=b.symbol")
    df = dbdf.df()
    df[f'LTP {arrow}'] = df['ltp'] > df['high'].shift(1)
    # df = df.set_index('timestamp')
    df = df[['timestamp','close','ltp',f'LTP {arrow}','supertrend10','supertrend','20 CXover','MA20 SuP','Above ST11','Above ST10','ATR',f'ATR {arrow}','ma20SL_ge4','RSI',f'RSI {arrow}','CVD',f'CVD {arrow}']].rename(columns={'ltp':'LTP','timestamp':'Time','supertrend':'ST_11','supertrend10':'ST_10','20 CXover':'20 CXvr','ATR':'ATR (10)'})
    # df = df.reset_index(drop=True)
    # df.index.name = None
    df = df.sort_values(by='Time', ascending=False)
    df = df.head(20)    


    return print(df)




if __name__ == '__main__':
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2IwS1hBc1pRa2Ftb3psUGhZX1M0S2x1RklJMWx3dmpxd2xRcXU5Y0JXRDVqTHNxOXRaUV9yanhrekRlOEFIeENFSE90a1ZxYWFFc2RLOVd5SU5fYTlSLVR3TVR1ZHByblAwSUFvY1BNMUpXSnQ2bz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUyMTkzODAwLCJpYXQiOjE3NTIxMjIwMDcsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MjEyMjAwNywic3ViIjoiYWNjZXNzX3Rva2VuIn0.aTfEWjfWjJeCJSKXbXuFh8XTv_NIchtUX2yMIlMreww"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")
    symb1 = "NSE:NIFTY2571025350CE"
    symbl2 = "NSE:NIFTY2571025550PE"
    ce = start_bot(symb1,fyers)
    print(ce)
