'''
Created on Aug 9, 2023

@author: ayan
'''
from fyers_apiv3 import fyersModel
from fyers_api import accessToken

client_id = "15YI17TORX-100"
access_token = "S5XP6AHG26"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"

# fyers = fyersModel.FyersModel(client_id=client_id,token=access_token)



session =accessToken.SessionModel(
    client_id=client_id,
    secret_key=access_token,
    redirect_uri=redirect_uri,
    response_type=response_type)
# data = {
#     "symbol":"NSE:SBIN-EQ",
#     "resolution":"D",
#     "date_format":"0",
#     "range_from":"1622097600",
#     "range_to":"1622097685",
#     "cont_flag":"1"
# }
#
# response = fyers.history(data=data)
# print(response)

resp = session.generate_authcode()
print(resp)