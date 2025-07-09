from fyers_apiv3 import fyersModel
import duckdb as db
import pandas as pd
from flask import session as flask_session  # Use Flask session

client_id = "15YI17TORX-100"
access_token = None

def gen_AcessTok(auth_code):
    global access_token
    if access_token is None:
        secret_key = "2HJ9AD57A5"
        redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type="code",
            grant_type="authorization_code"
        )
        session.set_token(auth_code)
        access_token = session.generate_token()["access_token"]
    return access_token


def fryers_chain(auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
    data = {
        "symbol": "NSE:NIFTY50-INDEX",
        "strikecount": 30,
    }
    response = fyers.optionchain(data=data)
    return response


def selectStrike(df):
    db.sql("CREATE OR REPLACE TABLE df_ltp AS SELECT * FROM df")  # DuckDB in-memory
    dfd_ce = db.query("SELECT min(symbol) AS ce_sm FROM df_ltp WHERE ltp >= 150 AND ltp <= 250 AND option_type = 'CE'").df()
    dfd_pe = db.query("SELECT max(symbol) AS pe_sm FROM df_ltp WHERE ltp >= 150 AND ltp <= 250 AND option_type = 'PE'").df()

    ce = dfd_ce.iloc[0, 0] if not dfd_ce.empty else None
    pe = dfd_pe.iloc[0, 0] if not dfd_pe.empty else None
    # ce = "NSE:NIFTY2571025450CE"
    # pe = "NSE:NIFTY2571025550PE"
    return [ce, pe]


symbol_cache = {}

def loadSymbol(auth_code, use_flask_session=True):
    # ✅ Use flask session only when inside a web request
    # if use_flask_session:
    #     from flask import session as flask_session
    #     if 'ce_symbol' in flask_session and 'pe_symbol' in flask_session:
    #         return flask_session['ce_symbol'], flask_session['pe_symbol']

    # ✅ CLI or fallback global cache... use thsi for one session of app.py run(the strike data will persist here for one session)
    if 'ce' in symbol_cache and 'pe' in symbol_cache:
        return symbol_cache['ce'], symbol_cache['pe']

    resp = fryers_chain(auth_code)
    df_op = pd.DataFrame(resp["data"]["optionsChain"])
    columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask", "volume"]
    df_op = df_op[columns]

    ce, pe = selectStrike(df_op)

    # Store in global cache
    symbol_cache['ce'] = ce
    symbol_cache['pe'] = pe

    # Also store in flask session if inside Flask context
    # if use_flask_session:
    #     flask_session['ce_symbol'] = ce
    #     flask_session['pe_symbol'] = pe
    # print(ce,pe)
    return ce, pe
