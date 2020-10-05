import json
import hashlib

from flask_restful import Resource, reqparse
from datetime import datetime
from bson import ObjectId
from bson.json_util import dumps
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from flask_dir import mongo
from flask_dir.utils.validation import check_email_field, check_password, check_empty_field
from flask_dir.utils.decorators import current_user_permission
from .utils import id_exist


class User(Resource):
    def get(self):
        try:

            result = mongo.db.users.find({"status": "active"})
            data = ({"status":
                     {
                         "code": 200,
                         "message": "Successfully Retrieved"
                     },
                     "results": json.loads(dumps(result))}), 200
            return data

        except Exception as e:
            data = ({"status":
                     {
                         "code": 500,
                         'message': 'Some Error Occur'
                     },
                     "results": str(e)}), 500
            return data


class UserWithParameter(Resource):
    @jwt_required
    @current_user_permission(access_level=['admin_update'])
    def post(self, id):
        user = id_exist(id)
        if user['status'] == 'empty':
            return user['result']

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'first_name', location='json')
        parser.add_argument(
            'last_name', location='json')
        parser.add_argument(
            'username', location='json')
        parser.add_argument(
            'email', type=check_email_field,  help='Please enter email address', location='json', nullable=False, required=True)
        parser.add_argument(
            'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)
        parser.add_argument(
            'roles', location='json', action='append')
        parser.add_argument(
            'group', type=str, location='json')
        args = parser.parse_args(
            http_error_code=422)

        try:
            now = datetime.now()
            user = mongo.db.users.find_one(
                {"$or": [{'username': args.get('username')}, {'email': args.get('email')}]})

            if user and not str(user['_id']) == id:
                return {"status":
                        {
                            "code": 500,
                            "message": "Some Error Occurs"
                        },
                        "results": "Username or Email already exist"}, 500
            else:
                group = None
                if args.get('group'):
                    group = ObjectId(args.get('group'))
                data = {
                    "first_name": args.get('first_name'),
                    "last_name": args.get('last_name'),
                    "username": args.get('username'),
                    "email": args.get('email'),
                    "status": args.get('status'),
                    "group": group,
                    "updated_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                    "status_updated_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                }

                role_id = args['roles']
                role_obj = []
                if role_id is not None:
                    mongo.db.users.update_one(
                        {'_id': ObjectId(id)},
                        {
                            "$set": {
                                "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            },

                            "$unset": {
                                "roles": []
                            }
                        }
                    )
                    for i in range(0, len(role_id)):
                        role_obj.append(ObjectId(role_id[i]))

                data.update({"roles": role_obj})

                mongo.db.users.update_one(
                    {'_id': ObjectId(id)},
                    {
                        "$set": data
                    }
                )
                return {"status":
                        {
                            "code": 200,
                            "message": "User Updated successfully"
                        },
                        "results": []}, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500

    def delete(self, id):
        try:
            user = mongo.db.users.find_one(
                {"$and": [{'_id': ObjectId(id)}, {'status': "active"}]})

            if user is None:
                return {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404

            status = 'deleted'
            now = datetime.now()

            mongo.db.users.update_one(
                {'_id': ObjectId(id)},
                {
                    "$set": {
                        "status": status,
                        "status_updated_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                        "updated_at": now.strftime("%d/%m/%Y %H:%M:%S")
                    }
                }
            )

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
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500

    def get(self, id):
        try:
            user = id_exist(id)
            if user['status'] == 'empty':
                return user['result']
            else:
                return {"status":
                        {
                            "code": 200,
                            "message": "Successfully Retrived"
                        },
                        "results": json.loads(dumps(user['result']))}, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': "Some Error Occur"
                    },
                    "results": str(e)}, 500


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

            user = mongo.db.users.find_one(
                {"$and": [{"$or": [{'username': current_user}, {'email': current_user}]},
                          {'password': hashlib.sha256(
                              old_password.encode('utf-8')).hexdigest()}
                          ]})
            if user:
                mongo.db.users.update_one(
                    {'_id': user['_id']},
                    {
                        "$set": {
                            "password": hashlib.sha256(new_password.encode('utf-8')).hexdigest(),
                            "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
                    }
                )
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