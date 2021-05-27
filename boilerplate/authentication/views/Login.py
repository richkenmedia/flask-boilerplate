import hashlib
import json

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token
)

from boilerplate import db
from boilerplate.utils.validation import check_empty_field
from boilerplate.user.models import Users
from boilerplate.role.models import Roles
from boilerplate.permission.models import Permissions


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
            user = Users.query.filter(((Users.username == args.get(
                'username')) | (Users.email == args.get('email'))), Users.password == hashlib.sha256(
                password.encode('utf-8')).hexdigest(), Users.status == 'active').first()
            if user:
                permissions = []
                role = []
                roles_permission = []
                try:
                    for role_id in user.roles:
                        roles = Roles.query.get(role_id.id)
                        role.append(roles.name)
                        roles_permission.extend(roles.permissions)

                    roles_permission.extend(user.permissions)
                    permission_list = list(dict.fromkeys(roles_permission))
                    for i in range(0, len(permission_list)):

                        permission_details = Permissions.query.get(
                            permission_list[i].id)
                        permissions.append(permission_details.name)
                except Exception as e:
                    pass
                return {
                    "status": {
                        "code": 200,
                        "message": "User logged in successfully"
                    },

                    "results": {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'email': user.email,
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
