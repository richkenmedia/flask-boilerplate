from flask_restful import Resource, reqparse
from slugify import slugify

from boilerplate import db
from boilerplate.utils.validation import check_empty_field
from boilerplate.function.models import Functions
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


class FunctionUpdate(Resource):
    def put(self, id):
        args = parser.parse_args(
            http_error_code=422)
        try:
            function = Functions.query.get(id)
            if function is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404
            else:

                function.name = args.get('name')
                replacements = [['-', '_']]
                function.slug = slugify(
                    args.get('name'), replacements=replacements)
                function.status = args.get('status')
                function.permissions.clear()
                permission_data = Permissions.query.filter(
                    Permissions.id.in_(args['permissions'])).all()
                function.permissions.extend(permission_data)
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
