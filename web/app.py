from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', nav_bar='home')


@app.route('/manual_mode')
def manual_mode():
    return render_template('manualMode.htm', nav_bar='manual_mode')


@app.route('/training_mode')
def training_mode():
    return render_template('trainingMode.htm', nav_bar='training_mode')


@app.route('/autonomous_mode')
def autonomous_mode():
    return render_template('autonomousMode.htm', nav_bar='auto_mode')


if __name__ == '__main__':
    app.run(host='127.0.0.2', port=5000, debug=True)
