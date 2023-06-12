from flask import Flask
from flask_socketio import SocketIO

# from .middleware.communication import get_cam_feed

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)        # to run websockets for this flask app. A new server runs for this.
    
    """ ----------- Register blueprints -----------"""
    from .web import web as main_blueprint  # for displaying web-pages
    # from .feed import feed                  # for handling camera and ultra-sonic feed

    app.register_blueprint(main_blueprint, url_prefix='/')
    # app.register_blueprint(feed, url_prefix='/feed')

    return socketio, app
