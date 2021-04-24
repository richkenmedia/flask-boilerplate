from flask_restful import Resource, fields, marshal
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from boilerplate import db
# from boilerplate.utils.decorators import current_user_permission
from boilerplate.user.models import Users


class UserList(Resource):

    def get(self):
        try:

            permission_fields = {
                'id': fields.Integer,
                'name': fields.String
            }
            role_fields = {
                'id': fields.Integer,
                'name': fields.String,
                'permissions': fields.Nested(permission_fields),
            }
            user_fields = {
                'id': fields.Integer,
                'username': fields.String,
                'first_name': fields.String,
                'last_name': fields.String,
                'email': fields.String,
                'status': fields.String,
                'username': fields.String,
                'roles': fields.Nested(role_fields),
                'permissions': fields.Nested(permission_fields),
                'created_at': fields.DateTime(dt_format='iso8601'),
                'updated_at': fields.DateTime(dt_format='iso8601'),
                'created_by': fields.Integer,
                'updated_by': fields.Integer
            }
            users = Users.query.filter(Users.status == "active").all()
            results = marshal(users, user_fields)
            data = ({"status":
                     {
                         "code": 200,
                         "message": "Successfully Retrieved"
                     },
                     "results": results}), 200
            return data

        except Exception as e:
            data = ({"status":
                     {
                         "code": 500,
                         'message': 'Some Error Occur'
                     },
                     "results": str(e)}), 500
            return data
