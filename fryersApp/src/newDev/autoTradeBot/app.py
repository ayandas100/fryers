from flask import Flask, render_template, request, jsonify
from fetchStrikeData import start_bot
import pandas as pd
from fetchStrikeData import getAuthCode

app = Flask(__name__)
session = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    auth_url = getAuthCode()
    if request.method == 'POST':
        session['token'] = request.form['access_token']
        session['ce_symbol'] = request.form['ce_symbol']
        session['pe_symbol'] = request.form['pe_symbol']
        return render_template('result.html')  # triggers auto-refresh
    return render_template('index.html',auth_url=auth_url)

@app.route('/data')
def get_data():
    try:
        ce_table = start_bot(session['ce_symbol'], session['token'])
        pe_table = start_bot(session['pe_symbol'], session['token'])

        # ce_table = ce_df.to_html(classes='table table-bordered table-sm', index=False)
        # pe_table = pe_df.to_html(classes='table table-bordered table-sm', index=False)

        return jsonify({'ce_table': ce_table, 'pe_table': pe_table})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/result')
def result():
    ce_symbol = session.get('ce_symbol', 'Call Option (CE)')
    pe_symbol = session.get('pe_symbol', 'Put Option (PE)')
    return render_template('result.html', ce_symbol=ce_symbol, pe_symbol=pe_symbol)


if __name__ == '__main__':
    app.run(debug=True)