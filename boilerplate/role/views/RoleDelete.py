from flask_restful import Resource

from boilerplate import db
from boilerplate.role.models import Roles


class RoleDelete(Resource):
    def delete(self, id):
        try:
            role = Roles.query.get(id)
            if role is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404

            if role.name == 'admin' or role.name == 'user':
                return {"status":
                        {
                            "code": 500,
                            "message": "Cannot able to delete this role"
                        },
                        "results": []}, 500
            db.session.delete(role)
            db.session.commit()

            # now = datetime.now()
            # role.status = 'deleted'
            # role.deleted_at = now.strftime("%Y-%m-%d %H:%M:%S")
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
