from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes

role_blueprint = Blueprint('role', __name__, url_prefix='/api/role')
api = Api(role_blueprint)

initialize_routes(api)
