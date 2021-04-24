from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

forgot_password_blueprint = Blueprint(
    'forgot_password', __name__, url_prefix='/api/')
api = Api(forgot_password_blueprint)
initialize_routes(api)
