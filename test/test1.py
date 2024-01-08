import pandas as pd 
from sqlalchemy import create_engine
import mysql.connector

conn = create_engine("mysql://ayan_1:A380b747@127.0.0.1/tradedb")
df = pd.read_sql("select * from nifty_50 order by trade_date desc limit 5",conn)
print(df.head())