import datetime
import json


from flask_restful import Resource, reqparse
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_jwt_extended import (
    jwt_required
)
from flask_dir import mongo
from flask_dir.utils.decorators import current_user_permission
from flask_dir.utils.validation import check_empty_field
from .utils import id_exist, role_permission


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'description', location='json')
parser.add_argument(
    'name', type=check_empty_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
parser.add_argument(
    'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)
parser.add_argument(
    'permissions', location='json', action='append')


class Role(Resource):
    def get(self):
        try:
            result = mongo.db.roles.find()
            data = {"status":
                    {
                        "code": 200,
                        "message": "Successfully Retrived"
                    },
                    "results": json.loads(dumps(result))}

            return data, 200

        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500

    def post(self):
        args = parser.parse_args(
            http_error_code=422)
        try:

            now = datetime.datetime.now()
            result = mongo.db.roles.insert_one({
                "name": args.get('name'),
                "description": args.get('description'),
                'status': args.get('status'),
                "created_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                "updated_at": "",
                "created_by": "",
                "updated_by": "",
            })
            permission_id = args['permissions']
            if permission_id is not None:
                role_permission(permission_id, result.inserted_id)

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


class RoleWithParameter(Resource):
    def get(self, id):
        try:
            role = id_exist(id)
            if role['status'] == 'empty':
                return role['result']

            return {"status":
                    {
                        "code": 200,
                        "message": "Successfully Retrived"
                    },
                    "results": json.loads(dumps(role['result']))
                    }, 200

        except Exception as e:
            return {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}, 500

    def post(self, id):
        args = parser.parse_args(
            http_error_code=422)
        try:
            role = id_exist(id)
            if role['status'] == 'empty':
                return role['result']

            if role['result']['name'] == 'admin' or role['result']['name'] == 'user':
                name = role['name']
            else:
                name = args.get('name')

            now = datetime.datetime.now()
            mongo.db.roles.update_one(
                {'_id': ObjectId(id)},
                {
                    "$set": {
                        "name": name,
                        "description": args.get('description'),
                        "status": args.get('status'),
                        "updated_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                        "updated_by": "",
                    }
                }
            )

            mongo.db.roles.update_one(
                {'_id': ObjectId(id)},
                {
                    "$set": {
                        "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    },

                    "$unset": {
                        "permissions": []
                    }
                }
            )
            mongo.db.permissions.update_many(
                {"roles": ObjectId(id)},
                {
                    "$set": {
                        "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    },

                    "$pull": {
                        "roles": ObjectId(id)
                    },

                }

            )
            permission_id = args['permissions']
            if permission_id is not None:
                role_permission(permission_id, ObjectId(id))

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

    def delete(self, id):
        try:
            role = id_exist(id)
            if role['status'] == 'empty':
                return role['result']

            if role['result']['name'] == 'admin' or role['result']['name'] == 'user':
                return {"status":
                        {
                            "code": 500,
                            "message": "Cannot able to delete this role"
                        },
                        "results": []}, 500

            result = mongo.db.roles.delete_one(
                {"_id": ObjectId(id)})

            mongo.db.permissions.update_many(
                {"roles": ObjectId(id)},
                {
                    "$set": {
                        "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    },

                    "$pull": {
                        "roles": ObjectId(id)
                    },

                }

            )
            mongo.db.users.update_many(
                {"roles": ObjectId(id)},
                {
                    "$set": {
                        "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    },

                    "$pull": {
                        "roles": ObjectId(id)
                    },

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
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}, 500
