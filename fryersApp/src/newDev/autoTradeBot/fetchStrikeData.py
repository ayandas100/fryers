'''
Created on 29-Jun-2025

@author: User
'''
'''
Created on 13-Apr-2024

@author: User
'''
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
import duckdb as db
import pandas_ta as ta
from placeOrder import check_order_status

client_id = "15YI17TORX-100"
today = date.today().strftime("%Y-%m-%d")

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


def fryers_hist(symb,auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {"symbol": f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": "2025-06-26", "range_to": today, "cont_flag": "1"}

    candle_data = fyers.history(data)
    return candle_data

def fryers_chain(auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {
        "symbol":"NSE:NIFTY50-INDEX",
        "strikecount":3,
        
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
    df_ltp = df_op[columns]
    
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
    df = df_candle
    df["symbol"] = symb
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['Above_MA20'] = df['close'] > df['MA20']
    df = df[['symbol','timestamp','open','close','SUPERT_11_2.0','MA20','Above_MA20']].rename(columns={'SUPERT_11_2.0':'supertrend'})
    df_hist = df.sort_values(by='timestamp', ascending=False)
    # print(df_hist.head(20))
    
    dbdf = db.query("select a.*,b.ltp " \
"               from df_hist a" \
"               join df_ltp b" \
"               on a.symbol=b.symbol")
    df = dbdf.df()
    df = df.head(20)

    fyers = fryersOrder(auth_code)
    check_order_status(fyers)
    
    styled_html = df.style.apply(highlight_supertrend, axis=1).format(precision=2).to_html(index=False,table_attributes='class="table table-bordered table-hover table-sm"')


    return styled_html





