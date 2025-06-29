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

client_id = "15YI17TORX-100"
secret_key = "2HJ9AD57A5"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"
grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")



access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb1lUcndPa3VlaDdlTjRfSFJITFVnYkJyU3dQdUhldHc2SlUzZy0zR2dGTUUxS3k2cm5yUWJ1WjRBdjFXUE9wLUc4ZjdXTlp3OVktdkdLZ0VGMGM1SzRjd0g2VU1jbXNsakFYM2wzczVuQXhmd0VUbz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxMjQzNDAwLCJpYXQiOjE3NTEyMDI1NDQsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTIwMjU0NCwic3ViIjoiYWNjZXNzX3Rva2VuIn0.nBWqfNcTZO7uqYbjScLnHK0Uij-NH6-ynnk3dQHht8Q"
fyers = fyersModel.FyersModel(
    client_id=client_id, token=access_token, log_path="")

data = {
    "symbol":"NSE:NIFTY50-INDEX",
    "strikecount":3,
    
}
response = fyers.optionchain(data=data);
# print(json.dumps(response))
df = pd.DataFrame(response["data"]["optionsChain"])
columns = [
    "symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]

df = df[columns]
df_ce = db.query("select * from df where option_type='CE'").to_df()
df_pe = db.query("select * from df where option_type='PE'").to_df()

# print(df_ce.head(10))
# print(df_pe.head(10))


### read the data for selected strike price
#NSE:NIFTY2570325600CE 
data = {"symbol": "NSE:NIFTY2570325600CE", "resolution": "15", "date_format": "1",
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



print(df_candle.head(30))












