'''
Created on Aug 11, 2023

@author: ayan
'''
from datetime import date
from fyers_api import fyersModel
from fyers_api import accessToken
import os
# from dotenv import load_dotenv
from fyers_api.Websocket import ws
import datetime as dt
# load_dotenv()

client_id = "N3VPS274OH-100"
secret_key = "MONNT2QWHX"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"
grant_type = "authorization_code"

today = date.today().strftime("%Y-%m-%d")


def get_access_token():
    access = ""
    if not os.path.exists("./authcode"):
        print("Creating authcode directory")
        os.makedirs("./authcode")

    if not os.path.exists(f"authcode/{today}.txt"):
        session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key,
                                           redirect_uri=redirect_uri, response_type="code", grant_type="authorization_code")
        response = session.generate_authcode()
        print("Login Url : ", response)
        auth_code = input("Enter Auth Code : ")
        session.set_token(auth_code)
        access_token = session.generate_token()["access_token"]
        with open(f"authcode/{today}.txt", "w") as f:
            f.write(access_token)
    else:
        with open(f"authcode/{today}.txt", "r") as f:
            access = f.read()
    return access
access_token = get_access_token()
print(access_token)

fyers = fyersModel.FyersModel(
    client_id=client_id, token=access_token, log_path=os.getcwd())

data = {"symbol": "NIFTY50-INDEX", "resolution": "5", "date_format": "1",
         "range_from": "2023-01-18", "range_to": "2023-01-18", "cont_flag": "1"}

print(fyers.history(data))
 


#current epoch time
#open value
#highest value
#lowest value
#close value
#total traded quantity
 
