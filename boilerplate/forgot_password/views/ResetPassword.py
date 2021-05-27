import hashlib
import datetime

from flask import request
from flask_restful import Resource, reqparse

from boilerplate import db, mail
from boilerplate.utils.validation import check_password, check_empty_field
from boilerplate.user.models import UserDetails, Users


class ResetPassword(Resource):
    def post(self):
        reset_password_parser = reqparse.RequestParser(bundle_errors=True)
        reset_password_parser.add_argument(
            'password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
        reset_password_parser.add_argument(
            'confirm_password', type=check_password, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
        reset_password_parser.add_argument(
            'password_token', type=check_empty_field, help='Token is required', location='json', nullable=False, required=True)
        reset_password_args = reset_password_parser.parse_args(
            http_error_code=422)
        try:
            uuid = str(reset_password_args.get('password_token'))
            password = str(reset_password_args.get('password'))
            confirm_password = str(reset_password_args.get('confirm_password'))

            if password != confirm_password:
                return {
                    'message': {
                        "password": "New Password and Confirm Password should be same",
                        "confirm_password": "New Password and Confirm Password should be same",

                    }

                }, 422

            user_details = UserDetails.query.filter(
                UserDetails.uuid == uuid).first()
            if user_details:
                user = Users.query.filter(
                    Users.id == user_details.user_id).first()
                user.password = hashlib.sha256(
                    password.encode('utf-8')).hexdigest()
                db.session.commit()
                user_details.uuid = None
                db.session.commit()

                return {"status":
                        {
                            "code": 200,
                            "message": "Successfully Reset Password"
                        },
                        "results": "Successfully Reset Password"}, 200

            else:
                return {"status":
                        {
                            "code": 500,
                            "message": "Some Error Occur"
                        },
                        "results": "Token Expried! You Cannot Able to Reset Password Now"}, 500
        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        "message": "Some Error Occur"
                    },
                    "results": "You Cannot Able to Reset Password Now"}, 500
