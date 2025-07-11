from flask import Flask, render_template, request, jsonify, session as flask_session
from fetchStrikeData import start_bot,fryersOrder,print_bool_fields
import pandas as pd
from fetchStrikeData import getAuthCode
from placeOrder import get_order_state
from flask import request
import threading
from datetime import datetime
import time
import sys
import os
from orderStatusCurrent import get_current_order_details
import json
from symbolLoad import loadSymbol
from datetime import datetime
import time
import threading



app = Flask(__name__)
app.secret_key = 'supersecretkey'
session = {}
token = None 

@app.route('/', methods=['GET', 'POST'])
def index():
    auth_url = getAuthCode()
    if request.method == 'POST':
        session['token'] = request.form['access_token']
        flask_session['token'] = request.form['access_token']
        global token
        token = session['token']  
        # flask_session['ce_symbol'] = request.form['ce_symbol']
        # session['pe_symbol'] = request.form['pe_symbol']
        # session['stop_loss'] = float(request.form['stop_loss'])
        # session['target'] = float(request.form['target'])
        threading.Thread(target=wait_until_market_opens, daemon=True).start()
        return render_template('result.html')  # triggers auto-refresh
    return render_template('index.html',auth_url=auth_url)


# def getTok():
#     global token
#     token = session['token']        
#     return token

# def load_ce_pe_tables(token):
#     ce, pe = loadSymbol(token)
#     print("📦 Symbols:", ce, pe)
#     ce_table, ce_order_msg = start_bot(ce, token)
#     pe_table, pe_order_msg = start_bot(pe, token)
#     return ce, pe, ce_table, pe_table, ce_order_msg, pe_order_msg
    
# @app.route('/data')
# def get_data():
#     try:
#         # stop_loss = session['stop_loss']
#         # target = session['target']        
#         # token = getTok()
#         ce, pe = loadSymbol(token)
#         # ce, pe = loadSymbol(token)
#         # ce = session['ce_symbol']
#         # pe = session['pe_symbol']
    
#         # print("📦 Symbols:", ce, pe)
#         ce_table,ce_order_msg = start_bot(ce, token)
#         pe_table,pe_order_msg = start_bot(pe, token)
#         # ce, pe, ce_table, pe_table, ce_order_msg, pe_order_msg = load_ce_pe_tables(token)

#         # ce_table = ce_df.to_html(classes='table table-bordered table-sm', index=False)
#         # pe_table = pe_df.to_html(classes='table table-bordered table-sm', index=False)
#         # print("Returning data to frontend")
#         # print("CE Table:", ce_table[:200]) 
#         return jsonify({
#             'ce_table': ce_table,
#             'pe_table': pe_table,
#             'ce_symbol': ce,
#             'pe_symbol': pe,
#             'ce_order_msg': ce_order_msg,
#             'pe_order_msg': pe_order_msg
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)})


@app.route('/data')
def get_data():
    try:
        global token
        token = session.get('token')  # from flask session during login
        if not token:
            return jsonify({'error': 'Token not found in session.'})

        # ✅ Use from symbol_cache (filled by the thread after 9:15 AM)
        from symbolLoad import symbol_cache

        if 'ce' not in symbol_cache or 'pe' not in symbol_cache:
            return jsonify({'error': 'Symbols not loaded yet. Try after 9:15 AM.'})

        ce = symbol_cache['ce']
        pe = symbol_cache['pe']
        print("⚙️ Using cached symbols:", ce, pe)

        # Call your bot logic
        ce_table, ce_order_msg,df1 = start_bot(ce, token)
        pe_table, pe_order_msg,df2 = start_bot(pe, token)
        
        print("CE Fields")
        print_bool_fields(df1)
        print("PE Fields")
        print_bool_fields(df2)
        
        return jsonify({
            'ce_table': ce_table,
            'pe_table': pe_table,
            'ce_symbol': ce,
            'pe_symbol': pe,
            'ce_order_msg': ce_order_msg,
            'pe_order_msg': pe_order_msg
        })

    except Exception as e:
        return jsonify({'error': str(e)})




@app.route('/result')
def result():
    return render_template(
        'result.html',
        ce_symbol=session.get('ce_symbol', 'Call Option (CE)'),
        pe_symbol=session.get('pe_symbol', 'Put Option (PE)')
    )



@app.route('/order-status')
def order_status():
    return jsonify(get_order_state())



def auto_shutdown():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "15:15":
            print("It's (3:15pm) end of session. Exiting Flask app.")
            os._exit(0)  # Immediately stops the process
        time.sleep(30)


@app.route('/order-status-current')
def order_status_current():
    try:
        fyers = fryersOrder(token)
        orders_json = get_current_order_details(fyers)
        orders = json.loads(orders_json)
        return render_template("order_status_current.html", orders=orders)
    
    except Exception as e:
        return f"Error: {e}", 500

# global_token must be set after login POST

# symbol_cache = {}

def wait_until_market_opens():
    global token
    while True:
        now = datetime.now().time()
        start_time = datetime.strptime("09:15", "%H:%M").time()
        end_time = datetime.strptime("21:14", "%H:%M").time()

        # Check if it's after 9:15 AND token is available
        if start_time <= now <= end_time and token:
            print("✅ It's 9:15 AM. Token is available. Loading symbols...")
            try:
                loadSymbol(token)
                print("✅ Symbols loaded successfully after 9:15 AM.")
            except Exception as e:
                print("❌ Error loading symbols:", str(e))
            break
        else:
            print("🕒 Waiting for market to open...")

        time.sleep(30)





if __name__ == '__main__':

    threading.Thread(target=auto_shutdown, daemon=True).start()
    app.run(debug=True)