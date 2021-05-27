
from flask_restful import Resource, reqparse

from boilerplate import db
from boilerplate.utils.validation import check_empty_field
from boilerplate.permission.models import Permissions


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'name', type=check_empty_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
parser.add_argument(
    'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)


class PermissionCreate(Resource):

    def post(self):
        args = parser.parse_args(
            http_error_code=422)
        try:
            permission = Permissions(
                name=args.get('name'),
                status=args.get('status')
            )

            db.session.add(permission)
            db.session.commit()

            data = {"status":
                    {
                        "code": 200,
                        "message": "Successfully Created"
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
