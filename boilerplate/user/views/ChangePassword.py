import json
import hashlib

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from boilerplate import db
from boilerplate.utils.validation import check_password
from boilerplate.user.models import Users


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        change_password_parser = reqparse.RequestParser(bundle_errors=True)

        change_password_parser.add_argument(
            'old_password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
        change_password_parser.add_argument(
            'new_password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
        change_password_parser.add_argument(
            'confirm_password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
        change_password_args = change_password_parser.parse_args(
            http_error_code=422)
        try:
            old_password = change_password_args.get('old_password')
            new_password = change_password_args.get('new_password')
            confirm_password = change_password_args.get('confirm_password')

            if new_password != confirm_password:
                return {
                    'message': {
                        "new_password": "New Password and Confirm Password should be same",
                        "confirm_password": "New Password and Confirm Password should be same",

                    }

                }, 422
            current_user = get_jwt_identity()
            user = Users.query.filter((Users.username == current_user) | (
                Users.email == current_user), Users.password == hashlib.sha256(
                old_password.encode('utf-8')).hexdigest()).first()

            if user:
                user.password = hashlib.sha256(
                    new_password.encode('utf-8')).hexdigest()
                db.session.commit()
                return {"status":
                        {
                            "code": 200,
                            'message': 'Change Password Successfully'
                        },
                        "results": []
                        }, 200
            return {
                'message': {
                    "old_password": "Please Enter Correct Old Password",

                }

            }, 422
        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}, 500
