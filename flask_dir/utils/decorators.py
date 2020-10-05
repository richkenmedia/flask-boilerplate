
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import Forbidden

from flask_dir import mongo


def current_user_permission(access_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            permissions = []
            roles_permission = []
            username = get_jwt_identity()
            user = mongo.db.users.find_one({"$and": [
                                            {"$or": [{'username': username}, {'email': username}]}, {"roles": {"$exists": True}}]})
            if user:
                for role_id in user['roles']:
                    roles = mongo.db.roles.find_one(
                        {'_id': role_id})
                    roles_permission.extend(roles['permissions'])

                for i in range(0, len(list(dict.fromkeys(roles_permission)))):
                    permission_name = mongo.db.permissions.find_one(
                        {'_id': roles_permission[i]})
                    permissions.append(permission_name['name'])

                check = any(item in access_level for item in permissions)
                if check is True:
                    return func(*args, **kwargs)
            return {"status":
                    {
                        "code": 403,
                        'message': "You do not have access"
                    },
                    "results": []}, 403

        return wrapper
    return decorator
