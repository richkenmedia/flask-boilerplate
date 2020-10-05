from flask import Flask
from .extensions import mongo, mail, jwt


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py', silent=True)

    with app.app_context():
        mail.init_app(app)
        mongo.init_app(app)
        jwt.init_app(app)

        from .role_permission_seeder import RolePermissionSeeder

        from .user import user_blueprint
        app.register_blueprint(user_blueprint)

        from .authentication import authentication_blueprint
        app.register_blueprint(authentication_blueprint)

        from .role import role_blueprint
        app.register_blueprint(role_blueprint)

        from .permission import permission_blueprint
        app.register_blueprint(permission_blueprint)

        from .forgot_password import forgot_password_blueprint
        app.register_blueprint(forgot_password_blueprint)

    return app
