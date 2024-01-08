'''
Created on Aug 11, 2023

@author: ayan
'''
from datetime import datetime,date
from _datetime import timedelta

start_time = datetime.now()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("https://www.python.org")
print(driver.title)
end_time = datetime.now() - start_time
ed = datetime.strptime("{} {}".format(date.today(),end_time), "%Y-%m-%d %H:%M:%S.%f")
print(ed)
print(start_time.strftime())
