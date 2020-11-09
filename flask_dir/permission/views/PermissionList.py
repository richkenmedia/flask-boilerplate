from flask_restful import Resource, fields, marshal
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from flask_dir import db
from flask_dir.permission.models import Permissions
from flask_dir.utils.decorators import current_user_permission


class PermissionList(Resource):
    @jwt_required
    @current_user_permission('PermissionList-get')
    def get(self):
        try:
            permission_fields = {
                'id': fields.Integer,
                'name': fields.String,
                'status': fields.String,
                'created_at': fields.DateTime(dt_format='iso8601'),
                'updated_at': fields.DateTime(dt_format='iso8601'),
                'created_by': fields.Integer,
                'updated_by': fields.Integer,
            }
            permissions = Permissions.query.filter(
                Permissions.status == "active").all()
            results = marshal(permissions, permission_fields)

            data = {"status":
                    {
                        "code": 200,
                        "message": "Successfully Retrived"
                    },
                    "results": results}

            return data, 200

        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500
