from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_mail import Mail, Message

mongo = PyMongo()
mail = Mail()
jwt = JWTManager()
