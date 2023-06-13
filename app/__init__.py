from flask import Flask
# from .middleware.communication

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secret!'

    """ ----------- Register blueprints -----------"""
    from .web import web as main_blueprint  # for displaying web-pages
    from .feed import feed                  # for handling camera and ultra-sonic feed

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(feed, url_prefix='/feed')

    # global socketio
    # , logger=True, engineio_logger=True)        # to run websockets for this flask app. A new server runs for this.
    # socketio = SocketIO(app, cors_allowed_origins="*")
    # socketio.init_app(app, cors_allowed_origins="*")

    return app

# Get the event handlers
# print("[DEBUG] app: about to import other modules..")
# from .middleware.communication import handle_connect, handle_stream, handle_disconnect, get_cam_feed
# print("[DEBUG] app: Imported other modules..")
