from flask import render_template, Response
from . import feed

@feed.route('/ultra-sonic')
def ultrasonic_feed():
    return 'ultra-sonic feed'

@feed.route('/camera')
def camera_feed():
    return 'camera feed'