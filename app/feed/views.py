from flask import render_template, Response
from . import feed
from ..middleware.communication import get_processed_frames

## Routes
@feed.route('/ultra-sonic')
def ultrasonic_feed():
    return 'ultra-sonic feed'

@feed.route('/camera')
def camera_feed():
    return Response(get_processed_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')