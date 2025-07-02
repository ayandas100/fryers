from datetime import date
from fyers_api import fyersModel
from fyers_api import accessToken
import os
from fyers_apiv3 import fyersModel
import datetime as dt
import json
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
import duckdb as db
import pandas_ta as ta
from autoTradeBot.placeOrder import check_order_status,place_bo_order
from autoTradeBot.symbolLoad import loadSymbol

client_id = "15YI17TORX-100"
# secret_key = "2HJ9AD57A5"
# redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
# response_type = "code"  
# state = "sample_state"
# grant_type = "authorization_code"  
today = date.today().strftime("%Y-%m-%d")
symbol_list = []

access_token = None
def gen_AcessTok(auth_code):
    global access_token
    if access_token is None:
        secret_key = "2HJ9AD57A5"
        redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
        response_type = "code"  
        state = "sample_state"
        grant_type = "authorization_code"  

        # Create a session model with the provided credentials
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type=response_type,
            grant_type=grant_type
            
        )

        # Generate the auth code using the session model
        auth_codeURL = session.generate_authcode()
        print(auth_codeURL)
        auth_code=auth_code
        # Set the authorization code in the session object
        session.set_token(auth_code)

        # Generate the access token using the authorization code
        access_token = session.generate_token()["access_token"]
    return access_token

# symb_optionchain="NSE:NIFTY50-INDEX"


def highlight_supertrend(row):
    supertrend = row['supertrend']
    close = row['close']
    
    if pd.isna(supertrend) or pd.isna(close):
        return [''] * len(row)

    styles = [''] * len(row)
    
    # Get column index of 'supertrend'
    st_index = row.index.get_loc('supertrend')

    if supertrend < close:
        styles[st_index] = 'background-color: lightgreen'
    elif supertrend > close:
        styles[st_index] = 'background-color: lightcoral'

    return styles

# def calculate_atr(df, period=14):
#     df['H-L'] = df['High'] - df['Low']
#     df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
#     df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))

#     df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
#     df['ATR'] = df['TR'].rolling(window=period).mean()

#     return df[['High', 'Low', 'Close', 'ATR']]

def fryers_hist(symb,auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {"symbol": f"{symb}", "resolution": "5", "date_format": "1",
            "range_from": "2025-06-26", "range_to": today, "cont_flag": "1"}

    candle_data = fyers.history(data)
    return candle_data

def fryers_chain(auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

    data = {
        "symbol":"NSE:NIFTY50-INDEX",
        "strikecount":30,
        
    }
    response = fyers.optionchain(data=data)
    return response


def fryersOrder(auth_code):
    access_token = gen_AcessTok(auth_code)
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
    return fyers


def selectStrike(df):
    if not symbol_list:
        dfd_ce = db.query("select max(symbol) as ce_sm from df where ltp >= 150 and ltp <=200 and option_type = 'CE'").df()
        ce = dfd_ce.iloc[0, 0]
        symbol_list.append(ce)
        dfd_pe = db.query("select max(symbol) as pe_sm from df where ltp >= 150 and ltp <=200 and option_type = 'PE'").df()
        pe = dfd_pe.iloc[0, 0]
        symbol_list.append(pe)
        return symbol_list



def start_bot(symb,auth_code):
    ce,pe =  loadSymbol(auth_code, use_flask_session=False)
#     resp =  fryers_chain(auth_code)
#     # resp =  auth_code
#     # print(resp)
#     df_op = pd.DataFrame(resp["data"]["optionsChain"])
#     columns = ["symbol", "option_type", "strike_price", "ltp", "bid", "ask","volume"]
#     df_op = df_op[columns]
#     global symbl
#     symbl = selectStrike(df_op)
#     ### read the data for selected strike price
#     #NSE:NIFTY2570325600CE 
#     ### read the data for selected strike price
#     #NSE:NIFTY2570325600CE 
    
#     candle_data = fryers_hist(symb,auth_code)
#     columns_candle = ["timestamp", "open", "high", "low", "close", "volume"]
#     df_candle = pd.DataFrame(candle_data["candles"],columns=columns_candle)
   
#     df_candle["timestamp"] = (
#         pd.to_datetime(df_candle["timestamp"], unit="s", utc=True)
#         .dt.tz_convert("Asia/Kolkata")
#         .dt.strftime("%Y-%m-%d %H:%M:%S")
#     )

#     df_candle = df_candle.sort_values(by="timestamp").reset_index(drop=True)
#     df_candle.ta.supertrend(length=11, multiplier=2.0, append=True)
#     df_candle.ta.supertrend(length=10, multiplier=1.0, append=True)
#     df_candle["symbol"] = symb
   
#     df_candle = df_candle[['symbol','timestamp','open','close','SUPERT_11_2.0','SUPERT_10_1.0','high','low']].rename(columns={'SUPERT_11_2.0':'supertrend','SUPERT_10_1.0':'supertrend10'})
#     df_candle = df_candle.drop_duplicates(subset='timestamp', keep='first')

#     df_candle.loc[:, 'MA20'] = df_candle['close'].rolling(window=20).mean()
#     df_candle.loc[:,'Above_MA20'] = df_candle['close'] > df_candle['MA20']
#     df_candle.loc[:, 'prev_Above_MA20'] = df_candle['Above_MA20'].shift(1)
#     df_candle.loc[:,'20 CXover'] = (df_candle['Above_MA20'] == True) & (df_candle['prev_Above_MA20'] == False)
#     df_candle.loc[:,'Above ST11'] = df_candle['close'] > df_candle['supertrend']
#     df_candle.loc[:,'Above ST10'] = df_candle['close'] > df_candle['supertrend10']

#     df_candle['H-L'] = df_candle['high'] - df_candle['low']
#     df_candle['H-PC'] = abs(df_candle['high'] - df_candle['close'].shift(1))
#     df_candle['L-PC'] = abs(df_candle['low'] - df_candle['close'].shift(1))
#     df_candle['TR'] = df_candle[['H-L', 'H-PC', 'L-PC']].max(axis=1)
#     df_candle['ATR'] = df_candle['TR'].rolling(window=14).mean()


#     dbdf = db.query("select a.*,b.ltp " \
# "               from df_candle a" \
# "               join df_op b" \
# "               on a.symbol=b.symbol")
#     df = dbdf.df()
#     df = df[['timestamp','ltp','supertrend10','supertrend','20 CXover','Above ST11','Above ST10','ATR']].rename(columns={'ltp':'LTP','timestamp':'Time','supertrend':'ST 11','supertrend10':'ST 10'})

#     df = df.sort_values(by='Time', ascending=False)
    


    # fyers = fryersOrder(auth_code)
    # check_order_status(fyers)

    # latest = df.iloc[0]
    # print(latest)
    
    # ltp = df['LTP'].iloc[0]
    # stop_loss = ltp - 10
    # target = ltp + 15
    # qty = 1
    # symbol = symb
    # print(ltp,stop_loss,target,symbol)
    # place_bo_order(fyers, symbol, qty=1, stop_loss=stop_loss, target=target)
    


    return print(ce,pe)




if __name__ == '__main__':
    symb = "NSE:NIFTY2570325700PE"
    auth_code = input("Enter auth code: ")
    start_bot(symb,auth_code)