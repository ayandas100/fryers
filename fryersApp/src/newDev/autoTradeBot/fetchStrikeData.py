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


def highlight_supertrend(row):
    st_11 = row.get('ST_11')
    st_10 = row.get('ST_10')
    close = row.get('close')
    
    styles = [''] * len(row)
    
    if pd.notna(st_11) and pd.notna(close):
        st_11_index = row.index.get_loc('ST_11')
        if st_11 < close:
            styles[st_11_index] = 'background-color: lightgreen'
        elif st_11 > close:
            styles[st_11_index] = 'background-color: lightcoral'

    if pd.notna(st_10) and pd.notna(close):
        st_10_index = row.index.get_loc('ST_10')
        if st_10 < close:
            styles[st_10_index] = 'background-color: lightgreen'
        elif st_10 > close:
            styles[st_10_index] = 'background-color: lightcoral'

    return styles

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
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    df_candle = df_candle.sort_values(by="timestamp").reset_index(drop=True)
    df_candle.ta.supertrend(length=11, multiplier=2.0, append=True)
    df_candle.ta.supertrend(length=10, multiplier=1.0, append=True)
    df_candle["symbol"] = symb
   
    df_candle = df_candle[['symbol','timestamp','open','close','SUPERT_11_2.0','SUPERT_10_1.0','high','low']].rename(columns={'SUPERT_11_2.0':'supertrend','SUPERT_10_1.0':'supertrend10'})
    df_candle = df_candle.drop_duplicates(subset='timestamp', keep='first')

    df_candle.loc[:, 'MA20'] = df_candle['close'].rolling(window=20).mean()
    df_candle.loc[:,'Above_MA20'] = df_candle['close'] > df_candle['MA20']
    df_candle.loc[:, 'prev_Above_MA20'] = df_candle['Above_MA20'].shift(1)
    df_candle.loc[:,'20 CXover'] = (df_candle['Above_MA20'] == True) & (df_candle['prev_Above_MA20'] == False)
    df_candle.loc[:,'Above ST11'] = df_candle['close'] > df_candle['supertrend']
    df_candle.loc[:,'Above ST10'] = df_candle['close'] > df_candle['supertrend10']
    #ATR calculations
    df_candle['H-L'] = df_candle['high'] - df_candle['low']
    df_candle['H-PC'] = abs(df_candle['high'] - df_candle['close'].shift(1))
    df_candle['L-PC'] = abs(df_candle['low'] - df_candle['close'].shift(1))
    df_candle['TR'] = df_candle[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df_candle['ATR'] = df_candle['TR'].rolling(window=14).mean()
    # MA 20 Bounce calculation
    df_candle['prev_close'] = df_candle['close'].shift(1)
    df_candle['prev_low'] = df_candle['low'].shift(1)
    df_candle['prev_ma20'] = df_candle['MA20'].shift(1)
    df_candle['MA20_support_bounce_base'] = ((df_candle['prev_low'] <= df_candle['prev_ma20']) & (df_candle['prev_close'] > df_candle['prev_ma20']) &  (df_candle['close'] > df_candle['open']) & (df_candle['close'] > df_candle['MA20']))
    df_candle['MA20 SuP'] = (df_candle['MA20_support_bounce_base'] & (~df_candle['MA20_support_bounce_base'].shift(1).fillna(False)))                         


    dbdf = db.query("select a.*,b.ltp " \
"               from df_candle a" \
"               join df_op b" \
"               on a.symbol=b.symbol")
    df = dbdf.df()
    # df = df.set_index('timestamp')
    df = df[['timestamp','close','ltp','supertrend10','supertrend','20 CXover','MA20 SuP','Above ST11','Above ST10','ATR']].rename(columns={'ltp':'LTP','timestamp':'Time','supertrend':'ST_11','supertrend10':'ST_10'})
    # df = df.reset_index(drop=True)
    # df.index.name = None
    df = df.sort_values(by='Time', ascending=False)
    df = df.head(20)


    fyers = fryersOrder(auth_code)
    get_order_state()
    check_order_status(fyers)

    latest = df.iloc[0]
    previous = df.iloc[1]

    if (previous['20 CXover'] or previous['MA20 SuP'] or latest['20 CXover']) and latest['Above ST11'] and latest['Above ST10'] and latest['ATR'] >= 8.50:
        ltp = df['LTP'].iloc[0]
        stop_loss = 8
        atr = latest['ATR']
        target = 10 if 8.5 <= atr <= 12 else 15 if atr > 12 else 8
        qty = 1
        symbol = symb
        order_response = place_bo_order(fyers, symbol, qty, stop_loss, target)
    else:
        order_response = {
            "status": "skipped",
            "message": "Conditions not met for placing order."
        }

    

    styled_html = df.style.apply(highlight_supertrend, axis=1).format(precision=2)\
                    .set_table_styles(
                        [{'selector': 'td', 'props': [('white-space', 'normal'), ('word-wrap', 'break-word')]},
                        {'selector': 'th', 'props': [('white-space', 'normal'), ('word-wrap', 'break-word')]}]
                    )\
                    .to_html(table_attributes='class="table table-bordered table-hover table-sm w-100"')

   
    return styled_html,order_response





