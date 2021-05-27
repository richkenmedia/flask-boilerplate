from flask import Blueprint
from flask_restful import Api
from .routes import initialize_routes
from .models import *

permission_blueprint = Blueprint(
    'permission', __name__, url_prefix='/api/permission')
api = Api(permission_blueprint)

initialize_routes(api)
