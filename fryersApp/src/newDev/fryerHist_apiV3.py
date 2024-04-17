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

client_id = "N3VPS274OH-100"
secret_key = "MONNT2QWHX"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"
grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")


# def get_access_token():
#     access = ""
#     if not os.path.exists("./authcode"):
#         print("Creating authcode directory")
#         os.makedirs("./authcode")
#
#     if not os.path.exists(f"authcode/{today}.txt"):
#         session = fyersModel.SessionModel(
#             client_id=client_id,
#             secret_key=secret_key,
#             redirect_uri=redirect_uri,
#             response_type=response_type,
#             grant_type=grant_type
#
#         )
#         response = session.generate_authcode()
#         print("Login Url : ", response)
#         auth_code = input("Enter Auth Code : ")
#         session.set_token(auth_code)
#         access_token = session.generate_token()["access_token"]
#         with open(f"authcode/{today}.txt", "w") as f:
#             f.write(access_token)
#     else:
#         with open(f"authcode/{today}.txt", "r") as f:
#             access = f.read()
#     return access
# access_token = get_access_token()
# # access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MTI5ODAyNzEsImV4cCI6MTcxNDI2NDIxMSwibmJmIjoxNzEyOTgwMjcxLCJhdWQiOlsiZDoxIiwiZDoyIl0sInN1YiI6InJlZnJlc2hfdG9rZW4iLCJhdF9oYXNoIjoiZ0FBQUFBQm1HZ0V2bFF0V3pTNDd1ckJUWllXSDNhZzk4aWNtN0dBQU9lRFZ5WnBpRndxTVhDdVVIM1had3RiS3hiTERxcXNmTi1yZjI3Y1RmRUg4RlQ1a0hGcm43RVgwSTZ3YVBBUndsOU54Rks0NnktS0g1TGs9IiwiZGlzcGxheV9uYW1lIjoiQVlBTiBEQVMiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIzODMwNDFlYjQ4MTkwZDEwYjliYjdhZDdkOWI1NTA5MDNhNmU0ZDlhZjEzOGFmYzcxNDQ0ZTgyMCIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.iBx7vBCTfUbJOsk5ubSj659dMzcOC3e_PUvJtQWIBa8"
# # print(access_token)

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MTMwODc2MTMsImV4cCI6MTcxMzE0MTAxMywibmJmIjoxNzEzMDg3NjEzLCJhdWQiOlsiZDoxIiwiZDoyIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbUc2UjlrbjI4TXR5bnVyYXVBZnAyVDNkaGRGancwbDRzVHJrZXVfWE13VXBMLXA4dWFPQ29Zb0tvQVl6TzNjc2RmNlNUdncxUTJUdnc4WmJOQUM3eHdTUFdDcEFGV0xmLTNONVR3U1lXWTFXZjN4UT0iLCJkaXNwbGF5X25hbWUiOiJBWUFOIERBUyIsIm9tcyI6IksxIiwiaHNtX2tleSI6IjM4MzA0MWViNDgxOTBkMTBiOWJiN2FkN2Q5YjU1MDkwM2E2ZTRkOWFmMTM4YWZjNzE0NDRlODIwIiwiZnlfaWQiOiJYQTY2OTEwIiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.McqFm-drGILUgKng9368NhDhCJlR9EcdGSIJxFTG1nY"
fyers = fyersModel.FyersModel(
    client_id=client_id, token=access_token, log_path=os.getcwd())

data = {"symbol": "NSE:NIFTY50-INDEX", "resolution": "5", "date_format": "1",
         "range_from": "2023-01-18", "range_to": "2023-01-18", "cont_flag": "1"}

print(fyers.history(data))
 