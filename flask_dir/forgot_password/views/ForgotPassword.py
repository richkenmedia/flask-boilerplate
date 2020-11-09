import datetime
import hashlib

from flask import request, render_template
from flask_restful import Resource, reqparse
from flask_mail import Message

from flask_dir import db, mail
from flask_dir.utils.validation import check_email_field
from flask_dir.user.models import Users, UserDetails


class ForgotPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'email', type=check_email_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
        args = parser.parse_args(
            http_error_code=422)
        try:
            email = args.get('email')

            user = Users.query.filter(Users.email == email).first()

            if not user:
                return {
                    'message': {
                        "email": "Invalid Email Id",

                    }

                }, 422

            url = request.host_url + 'reset-password/'

            timestamp = datetime.datetime.now().timestamp()
            unique = str(user.id) + str(timestamp)
            uuid = hashlib.sha256(unique.encode()).hexdigest()
            user_details = UserDetails.query.filter(
                UserDetails.user_id == user.id).first()
            user_details.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_details.uuid = uuid
            db.session.commit()

            msg = Message("Reset Your Password",
                          recipients=[user.email],
                          )

            data = {
                'url': url + uuid,
                'user_name': user.username
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
