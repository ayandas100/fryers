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

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2EwTjdES1JuNEJRbkt2bDZSWk1vd2JoWkY0VG14R2xvWnI4LWdBSWg4bElIVnlzYnFzNWVka3pKQmpON0VRT2J5dGhkb1lGekg1VmJ1OFJWNWQ3STkxSnpjWGtjRThPWVNDNmJsWTlQZ0YxbkcyYz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxOTM0NjAwLCJpYXQiOjE3NTE4NjAwOTEsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTg2MDA5MSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.KKxoZsjxfaU5C5NzcgInn-WAIzMBmavcIRp_IKfhQoE"
fyers = fyersModel.FyersModel(
    client_id=client_id, token=access_token, log_path="")
#NSE:NIFTY50-INDEX
data = {
    "symbol":"NSE:NIFTY50-INDEX",
    "strikecount":3,
    
}
response = fyers.optionchain(data=data);
print(json.dumps(response))
df = pd.DataFrame(response["data"]["optionsChain"])
# columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]

# df = df[columns]
print(df.head(20)) 