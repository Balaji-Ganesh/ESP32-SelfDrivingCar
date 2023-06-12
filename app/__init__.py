from flask import Flask
from flask_socketio import SocketIO


socketio: SocketIO = SocketIO


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secret!'

    """ ----------- Register blueprints -----------"""
    from .web import web as main_blueprint  # for displaying web-pages
    # from .feed import feed                  # for handling camera and ultra-sonic feed

    app.register_blueprint(main_blueprint, url_prefix='/')
    # app.register_blueprint(feed, url_prefix='/feed')

    global socketio
    # , logger=True, engineio_logger=True)        # to run websockets for this flask app. A new server runs for this.
    socketio = SocketIO(app, cors_allowed_origins="*")

    return app


# Create the application..
app = create_app()
print("Application created")

# Get the event handlers
from .middleware.communication.web_communicator import handle_connect, handle_stream, handle_disconnect
from .middleware.communication import get_cam_feed