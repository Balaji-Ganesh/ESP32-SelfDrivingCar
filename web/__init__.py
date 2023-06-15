# Perform monkey patching.. to support asynchronous behaviour
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from .middleware.communication import esp32_comm, web_comm
socketio = SocketIO()


def create_app():
    # App initialization..........
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secret!'

    """ ----------- Register blueprints -----------"""
    from .web import web as main_blueprint  # for displaying web-pages
    
    # Initialize socketio
    socketio.init_app(app=app, cors_allowed_origins="*", async_mode="eventlet")
    # , logger=True, engineio_logger=True)        # to run websockets for this flask app. A new server runs for this.

    # Register blueprints..
    app.register_blueprint(main_blueprint, url_prefix='/')
    
    return app

# Get the event handlers
# print("[DEBUG] app: about to import other modules..")
# from .middleware.communication import handle_connect, handle_stream, handle_disconnect, get_cam_feed
# print("[DEBUG] app: Imported other modules..")
