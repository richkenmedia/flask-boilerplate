import hashlib

from flask_restful import Resource, reqparse
from datetime import datetime

from boilerplate import db
from boilerplate.utils.validation import check_email_field, check_password
from boilerplate.user.models import Users, UserDetails
from boilerplate.role.models import Roles


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'first_name', location='json')
        parser.add_argument(
            'last_name', location='json')
        parser.add_argument(
            'username', location='json')
        parser.add_argument(
            'email', type=check_email_field, help='Please enter email address',  location='json', nullable=False, required=True)
        parser.add_argument(
            'password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)

        args = parser.parse_args(
            http_error_code=422)

        try:
            password = args.get('password')
            now = datetime.now()
            user = Users.query.filter((Users.username == args.get(
                'username')) | (Users.email == args.get('email'))).first()

            if user:
                return {
                    "status": {
                        "code": 500,
                        "message": "Some Error Occurs"
                    },
                    "results": "User Already Exists"
                }, 500
            else:

                user = Users(
                    username=args.get('username'),
                    email=args.get('email'),
                    first_name=args.get('first_name'),
                    last_name=args.get('last_name'),
                    password=hashlib.sha256(
                        password.encode('utf-8')).hexdigest(),
                    status='inactive',
                )
                roles = Roles.query.filter(Roles.name == 'user').first()
                if roles:
                    user.roles.append(roles)

                db.session.add(user)
                db.session.commit()

                user_details = UserDetails(
                    user_id=user.id,
                    status='inactive',
                )
                db.session.add(user_details)
                db.session.commit()

                return {"status":
                        {
                            "code": 200,
                            "message": "User Registered successfully"
                        },
                        "results": []}, 200
        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500
