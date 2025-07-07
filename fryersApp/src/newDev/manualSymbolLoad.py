from fyers_apiv3 import fyersModel
import duckdb as db
import pandas as pd
from flask import session as flask_session  # Use Flask session

client_id = "15YI17TORX-100"
access_token = None



def fryers_chain(fyers):
    # access_token = gen_AcessTok(auth_code)
    fyers = fyers
    data = {
        "symbol": "NSE:NIFTY50-INDEX",
        "strikecount": 30,
    }
    response = fyers.optionchain(data=data)
    return response


def selectStrike(df):
    db.sql("CREATE OR REPLACE TABLE df_ltp AS SELECT * FROM df")  # DuckDB in-memory
    dfd_ce = db.query("SELECT max(symbol) AS ce_sm FROM df_ltp WHERE ltp >= 120 AND ltp <= 190 AND option_type = 'CE'").df()
    dfd_pe = db.query("SELECT max(symbol) AS pe_sm FROM df_ltp WHERE ltp >= 120 AND ltp <= 190 AND option_type = 'PE'").df()

    ce = dfd_ce.iloc[0, 0] if not dfd_ce.empty else None
    pe = dfd_pe.iloc[0, 0] if not dfd_pe.empty else None
    return [ce, pe]


if __name__ == '__main__':
    # Replace with your actual access token
    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb2EwTjdES1JuNEJRbkt2bDZSWk1vd2JoWkY0VG14R2xvWnI4LWdBSWg4bElIVnlzYnFzNWVka3pKQmpON0VRT2J5dGhkb1lGekg1VmJ1OFJWNWQ3STkxSnpjWGtjRThPWVNDNmJsWTlQZ0YxbkcyYz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjYTU5M2UwOTRmZmIyMzBmZTNkMjdiNGY5NDA1Y2ZmOWM5ZmI2YzEzNjBmMDRjYTExMjY4OGMxMyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEE2NjkxMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzUxOTM0NjAwLCJpYXQiOjE3NTE4NjAwOTEsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc1MTg2MDA5MSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.KKxoZsjxfaU5C5NzcgInn-WAIzMBmavcIRp_IKfhQoE"

    # Initialize Fyers API
    fyers = fyersModel.FyersModel(client_id="15YI17TORX-100",token=ACCESS_TOKEN, log_path="")

    resp = fryers_chain(fyers)
    df_op = pd.DataFrame(resp["data"]["optionsChain"])
    columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask", "volume"]
    df_op = df_op[columns]

    ce, pe = selectStrike(df_op)

    print(ce,pe)