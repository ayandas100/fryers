'''
Created on 14-Apr-2024

@author: User
'''
'''
Created on Aug 11, 2023

@author: ayan
'''
from datetime import date
from fyers_apiv3 import fyersModel
import os
# from dotenv import load_dotenv
# from fyers_apiv3.FyersWebsocket import wb
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
mobnum = "9380951281"

today = date.today().strftime("%Y-%m-%d")


def get_access_token():
    access = ""
    session = fyersModel.SessionModel(client_id=client_id, secret_key=secret_key,redirect_uri=redirect_uri, response_type="code", grant_type="authorization_code")
    response = session.generate_authcode()

    driver.get(response)
    print("Login Url : ", response)
    mob = driver.find_element("id", "mobile-code")
    driver.implicitly_wait(1)
    mob.send_keys(mobnum)
    driver.implicitly_wait(1)
    submitMob = driver.find_element("id", "mobileNumberSubmit")
    submitMob.send_keys(Keys.ENTER)
    # auth_code = input("Enter Auth Code : ")
    driver.implicitly_wait(40)
    auth_code = driver.find_element("id", "s_auth_code")
    session.set_token(auth_code)
    # access_token = session.generate_token()["access_token"]
    access_token = session.generate_token()
    print(access_token)
    return access_token

if __name__ == "__main__":
    get_access_token()