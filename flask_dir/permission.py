import datetime
import json

from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask_dir import mongo
from flask_dir.utils.validation import check_empty_field

permission_blueprint = Blueprint(
    'permission', __name__, url_prefix='/api/permission')
api = Api(permission_blueprint)

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'name', type=check_empty_field, help='Please Enter Name Field', location='json', nullable=False, required=True)
parser.add_argument(
    'status', type=check_empty_field, help='This Field is required', location='json', nullable=False, required=True)


class Permission(Resource):
    def get(self):
        try:
            result = mongo.db.permissions.find()

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
            result = mongo.db.permissions.insert({
                "name": args.get('name'),
                'status': args.get('status'),
                "created_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                "updated_at": "",
                "created_by": "",
                "updated_by": "",
            })

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


api.add_resource(Permission, '')


class PermissionWithParameter(Resource):
    def id_exist(self, id):
        result = mongo.db.permissions.find_one({'_id': ObjectId(id)})
        if result is None:
            response = {"status":
                        {
                            "code": 404,
                            "message": "No Data Found"
                        },
                        "results": []}, 404
            return {
                'status': 'empty',
                'result': response,
            }
        else:
            return {
                'status': 'not empty',
                'result': result,
            }

    def get(self, id):
        try:
            permission = self.id_exist(id)
            if permission['status'] == 'empty':
                return permission['result']

            return {"status":
                    {
                        "code": 200,
                        "message": "Successfully Retrived"
                    },
                    "results": json.loads(dumps(permission['result']))
                    }
        except Exception as e:
            data = {"status":
                    {
                        "code": 500,
                        'message': 'Some Error Occur'
                    },
                    "results": str(e)}
            return data, 500

    def post(self, id):
        args = parser.parse_args(
            http_error_code=422)
        try:
            permission = self.id_exist(id)
            if permission['status'] == 'empty':
                return permission['result']

            now = datetime.datetime.now()
            mongo.db.permissions.update_one(
                {'_id': ObjectId(id)},
                {
                    "$set": {
                        "name": args.get('name'),
                        'status': args.get('status'),
                        "updated_at": now.strftime("%d/%m/%Y %H:%M:%S"),
                        "updated_by": "",
                    }
                }
            )
            data = {"status":
                    {
                        "code": 200,
                        "message": "Updated Successfully"
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

    def delete(self, id):
        try:
            permission = self.id_exist(id)
            if permission['status'] == 'empty':
                return permission['result']

            result = mongo.db.permissions.delete_one(
                {"_id": ObjectId(id)})
            mongo.db.roles.update_many(
                {"permissions": ObjectId(id)},
                {
                    "$set": {
                        "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    },

                    "$pull": {
                        "permissions": ObjectId(id)
                    },

                }

            )
            data = {"status":
                    {
                        "code": 200,
                        "message": "Deleted Successfully"
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


api.add_resource(PermissionWithParameter, '/<string:id>')
