'''
Created on Jul 29, 2023

@author: ayan
'''
from nsetools import Nse
from pprint import pprint
import requests

url = "https://www1.nseindia.com/content/fo/fo_mktlots.csv"

def nse_headers():
    """
    Builds right set of headers for requesting http://nseindia.com
    :return: a dict with http headers
    """
    return {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'www1.nseindia.com',

            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'X-Requested-With': 'XMLHttpRequest'
            }

hd = nse_headers()
    
req = requests.get(url, headers=hd)
print(req.json())