from flask import Blueprint

# creating blueprint instance for feed module
feed = Blueprint('feed', __name__)

from . import views