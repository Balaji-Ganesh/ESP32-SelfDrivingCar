from flask import render_template, Response
from . import web

@web.route('/')
def home():
    return render_template('index.html', nav_bar='home')

@web.route('/manual_mode')
def manual_mode():
    return render_template('manualMode.htm', nav_bar='manual_mode')

@web.route('/training_mode')
def training_mode():
    return render_template('trainingMode.htm', nav_bar='training_mode')

@web.route('/autonomous_mode')
def autonomous_mode():
    return render_template('autonomousMode.htm', nav_bar='auto_mode')

# @web.route('/camfeed')
# def camfeed():
#     return  Response(parse_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
