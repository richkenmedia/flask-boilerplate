from flask import Blueprint
from flask_restful import Api
from .models import *

from .routes import initialize_routes

function_blueprint = Blueprint(
    'function', __name__, url_prefix='/api/function')
api = Api(function_blueprint)

initialize_routes(api)
