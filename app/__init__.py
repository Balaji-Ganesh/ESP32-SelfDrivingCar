from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='templates')
    
    """ ----------- Register blueprints -----------"""
    from .web import web as main_blueprint  # for displaying web-pages
    
    app.register_blueprint(main_blueprint, url_prefix='/')
    
    return app
