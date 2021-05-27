
from flask_restful import Resource

from boilerplate import db
from boilerplate.permission.models import Permissions


class PermissionDelete(Resource):

    def delete(self, id):
        try:
            permission = Permissions.query.get(id)
            if permission is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404
            db.session.delete(permission)
            db.session.commit()
            data = {"status":
                    {
                        "code": 200,
                        "message": "Deleted Successfully"
                    },
                    "results": []}
            return data, 200

        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500
