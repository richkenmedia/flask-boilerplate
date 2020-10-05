from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user/')
api = Api(user_blueprint)

initialize_routes(api)
