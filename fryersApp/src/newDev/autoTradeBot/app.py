from flask import Flask, render_template, request
# from supertrend_bot import start_bot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form['access_token']
        symbol = request.form['symbol']
        stop_loss = float(request.form['stop_loss'])
        target = float(request.form['target'])

        # Start your bot with these values
        start_bot(token, symbol, stop_loss, target)

        return "🚀 Bot Started Successfully!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)