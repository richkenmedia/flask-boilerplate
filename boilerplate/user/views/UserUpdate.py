import json

from flask_restful import Resource, reqparse
from datetime import datetime
# from flask_jwt_extended import (
#     jwt_required, get_jwt_identity
# )

from boilerplate import db
from boilerplate.utils.validation import check_email_field, check_empty_field
# from boilerplate.utils.decorators import current_user_permission
from boilerplate.user.models import Users
from boilerplate.role.models import Roles
from boilerplate.permission.models import Permissions


class UserUpdate(Resource):
    # @jwt_required
    # @current_user_permission(access_level=['admin_update'])
    def put(self, id):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'first_name', location='json')
        parser.add_argument(
            'last_name', location='json')
        parser.add_argument(
            'username', location='json')
        parser.add_argument(
            'email', type=check_email_field,  help='Please enter email address', location='json', nullable=False, required=True)
        parser.add_argument(
            'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)
        parser.add_argument(
            'roles', help='This Field is required', location='json', action='append', required=True)
        parser.add_argument(
            'permissions', help='This Field is required', location='json', action='append', required=True)
        args = parser.parse_args(
            http_error_code=422)

        try:
            user = Users.query.get(id)
            if user is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404

            user_exist = Users.query.filter((Users.username == args.get(
                'username')) | (Users.email == args.get('email'))).first()
            if user_exist and not user_exist.id == id:
                return {"status":
                        {
                            "code": 500,
                            "message": "Some Error Occurs"
                        },
                        "results": "Username or Email already exist"}, 500
            else:
                user.first_name = args.get('first_name')
                user.last_name = args.get('last_name')
                user.username = args.get('username')
                user.email = args.get('email')
                user.status = args.get('status')
                user.roles.clear()
                role_data = Roles.query.filter(
                    Roles.id.in_(args['roles'])).all()
                user.roles.extend(role_data)

                user.permissions.clear()
                permission_data = Permissions.query.filter(
                    Permissions.id.in_(args['permissions'])).all()
                user.permissions.extend(permission_data)

                db.session.commit()

                return {"status":
                        {
                            "code": 200,
                            "message": "User Updated successfully"
                        },
                        "results": []}, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500
