import os
import datetime


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS')
SECRET_KEY = os.environ.get('SECRET_KEY')

JWT_BLACKLIST_ENABLED = os.environ.get('JWT_BLACKLIST_ENABLED')
JWT_BLACKLIST_TOKEN_CHECKS = os.environ.get('JWT_BLACKLIST_TOKEN_CHECKS')
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)

BUNDLE_ERRRORS = os.environ.get('BUNDLE_ERRRORS')

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
