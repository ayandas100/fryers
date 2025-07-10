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
import pandas as pd
import json


client_id = "15YI17TORX-100"
secret_key = "2HJ9AD57A5"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"
grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2JycFdMT3hHbEhBenlvbnphQnhnRWFEdWo0bGZLb1lHRGl1RzFRQmw3aGllWlBRMnllb0xRZTVBa09yMXl1cWxXblBnd3ZWYVctYTRyMkhyUXVzWEdTVWgzR2VKcnl1TnlNQzVBWGZEZDViQW83UT0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUyMTkzODAwLCJpYXQiOjE3NTIwODcxMjYsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MjA4NzEyNiwic3ViIjoiYWNjZXNzX3Rva2VuIn0.K8n44-hXEgz2idVLAr5_osxHIGpEpOhqbVAVip0Np7I"
fyers = fyersModel.FyersModel(
    client_id=client_id, token=access_token, log_path="")
#NSE:NIFTY50-INDEX
data = {
    "symbol":"NSE:NIFTY50-INDEX",
    "strikecount":3,
    "timestamp": "250710" 
    
}
response = fyers.optionchain(data=data);
print(json.dumps(response))
latest_expiry = response['data']['expiryData'][1]['date']
print(latest_expiry)

# df = pd.DataFrame(response["data"]["expiryData"])
# columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]

# df = df[columns]
# print(df.head(20)) 