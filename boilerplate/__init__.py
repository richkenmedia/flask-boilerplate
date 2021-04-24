from flask import Flask
from .extensions import mail, jwt, db, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py', silent=True)
    with app.app_context():

        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)
        jwt.init_app(app)

        from .common import common_blueprint
        app.register_blueprint(common_blueprint)

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

        from .function import function_blueprint
        app.register_blueprint(function_blueprint)

    return app
