from flask import Flask, render_template, request, jsonify, session as flask_session
from fetchStrikeData import start_bot,fryersOrder
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

app = Flask(__name__)
session = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    auth_url = getAuthCode()
    if request.method == 'POST':
        session['token'] = request.form['access_token']
        session['ce_symbol'] = request.form['ce_symbol']
        session['pe_symbol'] = request.form['pe_symbol']
        session['stop_loss'] = float(request.form['stop_loss'])
        session['target'] = float(request.form['target'])
        return render_template('result.html')  # triggers auto-refresh
    return render_template('index.html',auth_url=auth_url)

@app.route('/data')
def get_data():
    try:
        stop_loss = session['stop_loss']
        target = session['target']
        global token
        token = session['token']        
        ce, pe = loadSymbol(token, use_flask_session=True)
        # print("📦 Symbols:", ce, pe)
        ce_table,ce_order_msg = start_bot(ce, token)
        pe_table,pe_order_msg = start_bot(pe, token)

        # ce_table = ce_df.to_html(classes='table table-bordered table-sm', index=False)
        # pe_table = pe_df.to_html(classes='table table-bordered table-sm', index=False)

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
        ce_symbol=flask_session.get('ce_symbol', 'Call Option (CE)'),
        pe_symbol=flask_session.get('pe_symbol', 'Put Option (PE)')
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


if __name__ == '__main__':

    threading.Thread(target=auto_shutdown, daemon=True).start()
    app.run(debug=True)