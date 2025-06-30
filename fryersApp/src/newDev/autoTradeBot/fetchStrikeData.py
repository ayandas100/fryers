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


client_id = "15YI17TORX-100"
secret_key = "2HJ9AD57A5"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"
grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")




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


def start_bot(symb,token):
    access_token = token
    fyers = fyersModel.FyersModel(
        client_id=client_id, token=access_token, log_path="")

    # data = {
    #     "symbol":"NSE:NIFTY50-INDEX",
    #     "strikecount":3,
        
    # }
    # response = fyers.optionchain(data=data);
    # # print(json.dumps(response))
    # df = pd.DataFrame(response["data"]["optionsChain"])
    # columns = [
    #     "symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]

    # df = df[columns]
    # df_ce = db.query("select * from df where option_type='CE'").to_df()
    # df_pe = db.query("select * from df where option_type='PE'").to_df()

    # print(df_ce.head(10))
    # print(df_pe.head(10))


    ### read the data for selected strike price
    #NSE:NIFTY2570325600CE 
    data = {"symbol": f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": "2025-06-26", "range_to": "2025-06-27", "cont_flag": "1"}

    candle_data = fyers.history(data)
    columns_candle = ["timestamp", "open", "high", "low", "close", "volume"] 
    df_candle = pd.DataFrame(candle_data["candles"],columns=columns_candle)
    # df_candle["timestamp"] = pd.to_datetime(df_candle["timestamp"], unit='s').dt.strftime("%Y-%m-%d %H:%M:%S")

    df_candle["timestamp"] = (
        pd.to_datetime(df_candle["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    df_candle.ta.supertrend(length=11, multiplier=2.0, append=True)
    df = df_candle
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['Above_MA20'] = df['close'] > df['MA20']
    df = df[['timestamp','open','close','SUPERT_11_2.0','MA20','Above_MA20']].rename(columns={'SUPERT_11_2.0':'supertrend'})
    df = df.sort_values(by='timestamp', ascending=False)
    df = df.head(20)
    df.reset_index(drop=True, inplace=True)
    styled_html = df.style.apply(highlight_supertrend, axis=1).format(precision=2).to_html(index=False,table_attributes='class="table table-bordered table-hover table-sm"')

    # print(df_candle.head(20))

    return styled_html





