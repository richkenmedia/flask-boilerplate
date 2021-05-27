from flask_restful import Resource

from boilerplate import db
from boilerplate.function.models import Functions


class FunctionDelete(Resource):
    def delete(self, id):
        try:
            function = Functions.query.get(id)
            if function is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404

            db.session.delete(function)
            db.session.commit()

            # now = datetime.now()
            # function.status = 'deleted'
            # function.deleted_at = now.strftime("%Y-%m-%d %H:%M:%S")
            # db.session.commit()
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
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}, 500
