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

client_id = "15YI17TORX-100"
secret_key = "2HJ9AD57A5"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"
grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb1lqdjY5V3RQRXVYT1BaVWFHVVVLd252RGpXUk1YWGhWcVY0UUJELVBvSHpEQkdzLWxHZjFkcm42TDdPUEltYy14SV9xcW5zU05zbTA2UzBKaUdpTjFFY3RtWHZEV0kybWJMMTJpQUN5dHczeXJobz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxMzI5ODAwLCJpYXQiOjE3NTEyNjgzNDYsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTI2ODM0Niwic3ViIjoiYWNjZXNzX3Rva2VuIn0.Ap_OHdeKmFS4zyy_So8I0qcPUVFmqw7z2fZLa4eCOog"
fyers = fyersModel.FyersModel(
    client_id=client_id, token=access_token, log_path="")
#NSE:NIFTY50-INDEX
data = {
    "symbol":"NSE:NIFTY2570325600CE",
    "strikecount":3,
    
}
response = fyers.optionchain(data=data);
# print(json.dumps(response))
df = pd.DataFrame(response["data"]["optionsChain"])
columns = [
    "symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]

df = df[columns]
print(df.head(20)) 