from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

authentication_blueprint = Blueprint(
    'authentication', __name__, url_prefix='/api/auth')
api = Api(authentication_blueprint)

initialize_routes(api)
