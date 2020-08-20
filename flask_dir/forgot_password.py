import json
import datetime
import hashlib

from flask import Blueprint, request, render_template, flash
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_mail import Message

from flask_dir import mongo, mail
from flask_dir.utils.validation import check_email_field, check_empty_field


forgot_password_blueprint = Blueprint(
    'forgot_password', __name__, url_prefix='/api/')
api = Api(forgot_password_blueprint)


class ForgotPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'email', type=check_empty_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
        args = parser.parse_args(
            http_error_code=422)
        try:
            email = args.get('email')

            user = mongo.db.users.find_one({'email': email})

            if not user:
                return {
                    'message': {
                        "email": "Invalid Email Id",

                    }

                }, 422

            url = request.host_url + 'reset-password/'

            timestamp = datetime.datetime.now().timestamp()
            unique = str(user['_id']) + str(timestamp)
            uuid = hashlib.sha256(unique.encode()).hexdigest()

            mongo.db.users.update_one(
                {'_id': user['_id']},
                {
                    "$set": {
                        "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "uuid": uuid}
                }
            )

            msg = Message("Reset Your Password",
                          recipients=[user['email']],
                          )

            data = {
                'url': url + uuid,
                'user_name': user['username']
            }
            msg.html = render_template('email/reset_password.html',
                                       data=data)
            mail.send(msg)
            return {"status":
                    {
                        "code": 200,
                        'message': 'Email Sent Successfully'
                    },
                    "results": []}, 200
        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500


api.add_resource(ForgotPassword, 'forgot-password')


class ResetPassword(Resource):
    def post(self):
        reset_password_parser = reqparse.RequestParser(bundle_errors=True)
        reset_password_parser.add_argument(
            'password', type=check_empty_field, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
        reset_password_parser.add_argument(
            'confirm_password', type=check_empty_field, help='Minimum six characters, at least one letter, one number and one special character', location='json', nullable=False, required=True)
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
                        "email": "New Password and Confirm Password should be same",

                    }

                }, 422

            user_details = mongo.db.users.find_one({'uuid': uuid})
            if user_details:
                mongo.db.users.update_one(
                    {'_id': user_details['_id']},
                    {
                        "$set": {
                            "password": hashlib.sha256(password.encode('utf-8')).hexdigest(),
                            "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        },
                        "$unset": {
                            "uuid": 1
                        }
                    }
                )
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


api.add_resource(ResetPassword, 'reset-password')
