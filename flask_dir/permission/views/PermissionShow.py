
from flask_restful import Resource, fields, marshal

from flask_dir import db
from flask_dir.utils.validation import check_empty_field
from flask_dir.permission.models import Permissions


class PermissionShow(Resource):

    def get(self, id):
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
            permission = Permissions.query.get(id)
            if permission is None:
                response = {"status":
                            {
                                "code": 404,
                                "message": "No Data Found"
                            },
                            "results": []}, 404
                return response
            else:
                results = marshal(permission, permission_fields)
                return {"status":
                        {
                            "code": 200,
                            "message": "Successfully Retrived"
                        },
                        "results": results
                        }, 200
        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500
