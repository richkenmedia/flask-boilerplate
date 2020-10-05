import datetime


from flask_dir import mongo
from bson import ObjectId


def id_exist(id):
    result = mongo.db.roles.find_one({'_id': ObjectId(id)})
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


def role_permission(permission_id, role_id):
    for i in range(0, len(permission_id)):
        mongo.db.roles.update_one(
            {'_id': role_id},
            {
                "$set": {
                    "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                },

                "$addToSet": {
                    "permissions": ObjectId(permission_id[i])
                }
            }
        )
        mongo.db.permissions.update_one(
            {'_id': ObjectId(permission_id[i])},
            {
                "$set": {
                    "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                },
                "$addToSet": {
                    "roles": role_id
                }
            }
        )
    return True
