# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import os, sys

from nsetools import Nse
import json
import pandas as pd
import requests
import mysql.connector
from py_topping.data_connection.database import lazy_SQL
import csv
from pprint import pprint
from sqlalchemy import create_engine



user = 'ayan_1'
passw = 'A380b747'
host =  '127.0.0.1'
port = 3306
database = 'tradedb'
my_conn = create_engine("mysql+mysqldb://ayan_1:A380b747@127.0.0.1/tradedb\
")
df_std = pd.DataFrame(
    columns=['_id', 'CH_SYMBOL', 'CH_TIMESTAMP', 'CH_SERIES', 'CH_MARKET_TYPE', 'CH_ISIN', 'CH_OPENING_PRICE',
             'CH_TRADE_HIGH_PRICE'])
df_std = pd.concat([df_std, pd.DataFrame(columns=['CH_TRADE_LOW_PRICE', 'CH_CLOSING_PRICE', 'CH_PREVIOUS_CLS_PRICE'])])
df_std = pd.concat(
    [df_std, pd.DataFrame(columns=['CH_LAST_TRADED_PRICE', 'VWAP', 'CH_52WEEK_HIGH_PRICE', 'CH_52WEEK_LOW_PRICE', ])])
df_std = pd.concat([df_std, pd.DataFrame(
    columns=['CH_52WEEK_LOW_PRICE', 'CH_TOT_TRADED_QTY', 'CH_TOT_TRADED_VAL', 'CH_TOTAL_TRADES', ])])

mode = 'local'

if(mode == 'local'):

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    }

def getNewColumnList(srcInputColList, tgtInputColList):
    newcollist = [i for i in tgtInputColList if i not in srcInputColList]
    newcollist.sort()
    return newcollist


def renameColumnsEquityHistory(df):
    coltodelete = getNewColumnList(df_std.columns, df.columns)
    # pprint(coltodelete)
    df = df.drop(coltodelete, axis='columns')
    df = df.rename(
        {'_id': 'trans_id', 'CH_SYMBOL': 'symbol_name', 'CH_TIMESTAMP': 'trade_date', 'CH_SERIES': 'series_name'},
        axis='columns')
    df = df.rename({'CH_MARKET_TYPE': 'market_type', 'CH_TRADE_HIGH_PRICE': 'day_high_price',
                    'CH_TRADE_LOW_PRICE': 'day_low_price'}, axis='columns')
    df = df.rename({'CH_OPENING_PRICE': 'day_open_price', 'CH_CLOSING_PRICE': 'day_close_price',
                    'CH_LAST_TRADED_PRICE': 'last_traded_price'}, axis='columns')
    df = df.rename({'CH_PREVIOUS_CLS_PRICE': 'prev_day_close_price', 'CH_52WEEK_HIGH_PRICE': 'fivetwoWeek_h_p',
                    'CH_52WEEK_LOW_PRICE': 'fivetwoWeek_l_p'}, axis='columns')
    df = df.rename({'CH_ISIN': 'isin_code', 'CH_TOT_TRADED_QTY': 'trade_volume', 'CH_TOTAL_TRADES': 'total_traded_nbr'},
                   axis='columns')
    df = df.rename({'CH_TOT_TRADED_VAL': 'trade_value', }, axis='columns')
    return df


def equity_history(symbol, series, start_date, end_date):
    payload = nsefetch("https://www1.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
    df = renameColumnsEquityHistory(pd.DataFrame.from_records(payload["data"]))
    return df


def nsefetch(payload):
    try:
        output = requests.get(payload, headers=headers).json()
           # print(output)
    except ValueError:
        s = requests.Session()
        output = s.get("https://www.nseindia.com", headers=headers)
        output = s.get(payload, headers=headers).json()
    return output


    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nse = Nse()
    df1 = pd.DataFrame()
    all_stock_codes = nse.get_stock_codes()
    print(len(all_stock_codes))
    print(all_stock_codes)
    today = datetime.date.today()
    # start_date = today + datetime.timedelta(days=-4)
    # -------------START start from any date---------
    initialStart_date_str = '01-01-2023'
    format_str = '%d-%m-%Y'  # The format
    datetime_obj = datetime.datetime.strptime(initialStart_date_str, format_str)
    # ------------- END start from any date---------
    start_date = datetime_obj.date()
    # start_date = todays
    start_date_str = start_date.strftime("%d-%m-%Y")
    end_date_str = today.strftime("%d-%m-%Y")
    for key in all_stock_codes:
        print("key>>" + key)
        if key.startswith("B") or key.startswith("C") or key.startswith("D") or key.startswith("E"):
        # if key.startswith("A") :
            if key != 'SYMBOL' or key != 'DVL' or key != 'DSSL':
                df = pd.DataFrame()
                print("IN FOR>" + key)
                print("start_date : " + start_date_str + " | end_date : " + end_date_str)
                symbol = key
                series = "EQ"
                df = equity_history(symbol, series, start_date_str, end_date_str)
                df.to_sql(con=my_conn, name='equity_history', if_exists='append', index=False)
                df1 = df1.append(df)
            # pprint(df)
    pprint(len(df1))
    pprint(df1)
    try:
        df1.to_sql(con=my_conn, name='equity_history', if_exists='append', index=False, chunksize = 140)
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
        pass
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
        pass
    my_conn.dispose()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
