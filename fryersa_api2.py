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

auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTE3NTcwMTUsImV4cCI6MTY5MTgwMDIxNSwibmJmIjoxNjkxNzU3MDE1LCJhdWQiOlsiZDoxIiwiZDoyIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazFpblhMWjExWlV3akl4V1RwUmdzVndNSi1Cd2w5T0VpZFBHMDY0LXRfbFVMc3JlZW8wUF8zVlVpX3NidjV1ZVl3VEk1LS1JTHpWWk9HWFk4Z2hBYVVxWlUtNEU0Z09pUUpvaGNWOFN1LWQwSWxkQT0iLCJkaXNwbGF5X25hbWUiOiJBWUFOIERBUyIsIm9tcyI6IksxIiwiaHNtX2tleSI6bnVsbCwiZnlfaWQiOiJYQTY2OTEwIiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.3ONGTPbT04mjJcps6hjvGBStsKgWKPU0uMhNr3O1m8A"

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
