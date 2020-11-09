from flask_restful import Resource, reqparse, fields, marshal

from flask_dir import db
from flask_dir.function.models import Functions


class FunctionShow(Resource):
    def get(self, id):
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
            function = Functions.query.get(id)
            if function is None:
                response = {"status":
                            {
                                "code": 404,
                                "message": "No Data Found"
                            },
                            "results": []}, 404
                return response
            else:
                results = marshal(function, function_fields)
                return {"status":
                        {
                            "code": 200,
                            "message": "Successfully Retrived"
                        },
                        "results": results}, 200
        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}, 500
