import pandas as pd 
from sqlalchemy import create_engine
import mysql.connector

conn = create_engine("mysql://ayan:A380b747@127.0.0.1/tradedb")
df = pd.read_sql("select * from nifty_history order by current_date_time desc limit 10",conn)
print(df.head())

