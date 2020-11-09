from flask_restful import Resource, reqparse
from slugify import slugify

from flask_dir import db
from flask_dir.utils.validation import check_empty_field
from flask_dir.function.models import Functions
from flask_dir.permission.models import Permissions


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'name', type=check_empty_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
parser.add_argument(
    'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)
parser.add_argument(
    'permissions', help='This Field is required', location='json', action='append', required=True)


class FunctionCreate(Resource):
    def post(self):
        args = parser.parse_args(
            http_error_code=422)
        try:
            replacements = [['-', '_']]
            slug = slugify(args.get('name'), replacements=replacements)
            function = Functions(
                name=args.get('name'),
                slug=slug,
                status=args.get('status')
            )
            permission_data = Permissions.query.filter(
                Permissions.id.in_(args['permissions'])).all()
            function.permissions.extend(permission_data)
            db.session.add(function)
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
