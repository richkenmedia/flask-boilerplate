import hashlib
import json

from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime
from bson.json_util import dumps
from flask_jwt_extended import (
    create_access_token, jwt_required, get_raw_jwt
)

from skill_tracker import mongo, jwt
from skill_tracker.utils.validation import check_email_field, check_password, check_empty_field

authentication_blueprint = Blueprint(
    'authentication', __name__, url_prefix='/api/auth')
api = Api(authentication_blueprint)


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'first_name', location='json')
        parser.add_argument(
            'last_name', location='json')
        parser.add_argument(
            'username', location='json')
        parser.add_argument(
            'email', type=check_email_field, help='Please enter email address',  location='json', nullable=False, required=True)
        parser.add_argument(
            'password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)

        args = parser.parse_args(
            http_error_code=422)

        try:
            roles = mongo.db.roles.find_one({'name': 'tenant'})
            status = "active"
            password = args.get('password')
            now = datetime.now()
            user = mongo.db.users.find_one(
                {"$or": [{'username': args.get('username')}, {'email': args.get('email')}]})

            if user:
                return {
                    "status": {
                        "code": 500,
                        "message": "Some Error Occurs"
                    },
                    "results": "User Already Exists"
                }, 500
            else:

                result = mongo.db.users.insert_one({
                    "username": args.get('username'),
                    "email":  args.get('email'),
                    "first_name": args.get('first_name'),
                    "last_name": args.get('last_name'),
                    "password": hashlib.sha256(password.encode('utf-8')).hexdigest(),
                    'status': status,
                    "status_updated_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                    "created_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": now.strftime("%d/%m/%Y %H:%M:%S")
                })
                if roles is not None:
                    mongo.db.users.update_one(
                        {'_id': result.inserted_id},
                        {
                            "$set": {
                                "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            },

                            "$addToSet": {
                                "roles": roles['_id']
                            }
                        }
                    )
                return {"status":
                        {
                            "code": 200,
                            "message": "User Registered successfully"
                        },
                        "results": []}, 200
        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500


api.add_resource(Register, '/register')


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'username', type=check_empty_field, help='Please enter your username', location='json', nullable=False, required=True)
        parser.add_argument(
            'password', type=check_empty_field, help='Please enter your password', location='json', nullable=False, required=True)

        args = parser.parse_args(
            http_error_code=422)

        username = args.get('username')
        password = args.get('password')
        try:
            user = mongo.db.users.find_one(
                {"$and": [{"$or": [{'username': username}, {'email': username}]},
                          {'password': hashlib.sha256(
                              password.encode('utf-8')).hexdigest()},
                          {'status': 'active'}
                          ]})
            if user:
                permissions = []
                role = []
                roles_permission = []
                try:
                    for role_id in user['roles']:

                        roles = mongo.db.roles.find_one(
                            {'_id': role_id})
                        role.append(roles['name'])

                        roles_permission.extend(roles['permissions'])

                    for i in range(0, len(list(dict.fromkeys(roles_permission)))):

                        permission_name = mongo.db.permissions.find_one(
                            {'_id': roles_permission[i]})
                        permissions.append(permission_name['name'])

                except Exception as e:
                    pass

                return {
                    "status": {
                        "code": 200,
                        "message": "User logged in successfully"
                    },

                    "results": {
                        'id': json.loads(dumps(user['_id'])),
                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': role,
                        'permission': permissions,
                        "access_token": create_access_token(identity=username),
                    }
                }, 200
            else:
                return {
                    "status": {
                        "code": 500,
                        "message": "Some Error Occur"
                    },
                    "results": "Invalid Credential"
                }, 500

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500


api.add_resource(Login, '/login')


class Logout(Resource):
    @jwt_required
    def delete(self):
        try:
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            return {
                "status": {
                    "code": 200,
                    "message": "Successfully logged out"
                },
                "results": []
            }, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500


api.add_resource(Logout, '/logout')
