from flask_dir.authentication.views.Register import Register
from flask_dir.authentication.views.Login import Login
from flask_dir.authentication.views.Logout import Logout


def initialize_routes(api):
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
