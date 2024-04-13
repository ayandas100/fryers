'''
Created on Aug 9, 2023

@author: ayan
'''
from fyers_api import fyersModel
from fyers_api import accessToken

client_id = "N3VPS274OH-100"
access_token = "MONNT2QWHX"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"


session =accessToken.SessionModel(
    client_id=client_id,
    secret_key=access_token,
    redirect_uri=redirect_uri,
    response_type=response_type)


resp = session.generate_authcode()
print(resp)