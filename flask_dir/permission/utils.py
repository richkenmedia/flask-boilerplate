
from flask_dir import mongo
from bson import ObjectId


def id_exist(id):
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
