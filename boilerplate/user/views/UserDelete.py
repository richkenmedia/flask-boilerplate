
from flask_restful import Resource
from datetime import datetime

from boilerplate import db
from boilerplate.user.models import Users


class UserDelete(Resource):
    def delete(self, id):
        try:
            user = Users.query.filter(Users.id == id,
                                      Users.status != 'deleted').first()
            if user is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404

            now = datetime.now()
            user.status = 'deleted'
            user.deleted_at = now.strftime("%Y-%m--%d %H:%M:%S")
            db.session.commit()
            return {"status":
                    {
                        "code": 200,
                        "message": "Deleted Successfully"
                    },
                    "results": []}, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500
