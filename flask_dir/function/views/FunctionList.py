
from flask_restful import Resource, fields, marshal

from flask_dir import db
from flask_dir.utils.validation import check_empty_field
from flask_dir.function.models import Functions


class FunctionList(Resource):
    def get(self):
        try:
            permission_fields = {
                'id': fields.Integer,
                'name': fields.String
            }
            function_fields = {
                'id': fields.Integer,
                'name': fields.String,
                'slug': fields.String,
                'status': fields.String,
                'permissions': fields.Nested(permission_fields),
                'created_at': fields.DateTime(dt_format='iso8601'),
                'updated_at': fields.DateTime(dt_format='iso8601'),
                'created_by': fields.Integer,
                'updated_by': fields.Integer,
            }
            functions = Functions.query.filter(
                Functions.status == "active").all()
            results = marshal(functions, function_fields)
            data = ({"status":
                     {
                         "code": 200,
                         "message": "Successfully Retrieved"
                     },
                     "results": results}), 200
            return data

        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500
