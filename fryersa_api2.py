'''
Created on Aug 11, 2023

@author: ayan
'''
from fyers_api import accessToken

client_id = "N3VPS274OH-100"
secret_key = "MONNT2QWHX"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"
grant_type = "authorization_code"

auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MDU2ODQ5NjQsImV4cCI6MTcwNTcxNDk2NCwibmJmIjoxNzA1Njg0MzY0LCJhdWQiOiJbXCJkOjFcIiwgXCJkOjJcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYQTY2OTEwIiwib21zIjoiSzEiLCJoc21fa2V5IjoiOTJlZmVhOGY2N2ZhYTE5ZTJkOWYyOTAwNGEyZDQ5ODJiOTc2Y2NhOWJjZGJmMTUzMWVmYmI3MmIiLCJub25jZSI6IiIsImFwcF9pZCI6Ik4zVlBTMjc0T0giLCJ1dWlkIjoiOGUwMGIwOGM2YzE1NDU2MmIwNDczZjNjM2ZlNWZjOTkiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.zgGs0fl31OSOWtA1Lt8nbjq6Tu1rBR_cGxicE_LaH5o"

session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)
session.set_token(auth_code)
response = session.generate_token()
print(response)
