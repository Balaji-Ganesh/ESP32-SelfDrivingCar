from flask import Flask

from .middleware.communication import get_cam_feed

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    """ ----------- Register blueprints -----------"""
    from .web import web as main_blueprint  # for displaying web-pages
    from .feed import feed                  # for handling camera and ultra-sonic feed

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(feed, url_prefix='/feed')

    return app
