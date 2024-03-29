from flask_restful import Resource, reqparse

from boilerplate import db
from boilerplate.utils.validation import check_empty_field
from boilerplate.role.models import Roles
from boilerplate.permission.models import Permissions

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'description', location='json')
parser.add_argument(
    'name', type=check_empty_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
parser.add_argument(
    'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)
parser.add_argument(
    'permissions', location='json', action='append')


class RoleUpdate(Resource):
    def put(self, id):
        args = parser.parse_args(
            http_error_code=422)
        try:
            role = Roles.query.get(id)
            if role is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404
            else:
                if role.name == 'admin' or role.name == 'user':
                    name = role.name
                else:
                    name = args.get('name')
                role.name = name
                role.description = args.get('description')
                role.status = args.get('status')
                role.permissions.clear()
                permission_data = Permissions.query.filter(
                    Permissions.id.in_(args['permissions'])).all()
                role.permissions.extend(permission_data)
                db.session.commit()

                return {"status":
                        {
                            "code": 200,
                            "message": "Data Updated successfully"
                        },
                        "results": []}, 200

            return {"status":
                    {
                        "code": 200,
                        "message": "Updated Successfully"
                    },
                    "results": []}, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}, 500
