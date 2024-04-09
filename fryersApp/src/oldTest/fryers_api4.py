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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()



client_id = "N3VPS274OH-100"
secret_key = "MONNT2QWHX"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"
grant_type = "authorization_code"

today = date.today().strftime("%Y-%m-%d")


def get_access_token():
    access = ""
    session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key,
                                       redirect_uri=redirect_uri, response_type="code", grant_type="authorization_code")
    response = session.generate_authcode()
    driver.get(response)
    print("Login Url : ", response)
    # auth_code = input("Enter Auth Code : ")
    driver.implicitly_wait(25)
    auth_code = driver.find_element("id", "s_auth_code")
    session.set_token(auth_code)
    # access_token = session.generate_token()["access_token"]
    access_token = session.generate_token()
    print(access_token)
    return access_token

if __name__ == "__main__":
    get_access_token()