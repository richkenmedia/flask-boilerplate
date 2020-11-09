from flask_restful import Resource, fields, marshal

from flask_dir import db
from flask_dir.user.models import Users


class UserShow(Resource):
    def get(self, id):
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
            user = Users.query.get(id)
            if user is None:
                response = {"status":
                            {
                                "code": 404,
                                "message": "No Data Found"
                            },
                            "results": []}, 404
                return response
            else:
                results = marshal(user, user_fields)
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
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500
