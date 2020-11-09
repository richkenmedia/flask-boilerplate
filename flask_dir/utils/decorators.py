
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from slugify import slugify


from flask_dir import db
from flask_dir.user.models import Users
from flask_dir.function.models import Functions
from flask_dir.role.models import Roles
from flask_dir.permission.models import Permissions


def current_user_permission(functiom_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = []
            permissions = []
            roles_permission = []
            access_level = []
            username = get_jwt_identity()
            slug = slugify(functiom_name, replacements=[['-', '_']])
            user = Users.query.filter((Users.username == username) | (
                Users.email == username)).first()
            function = Functions.query.filter((Functions.slug == slug)).first()
            if function is None:
                return {"status":
                        {
                            "code": 403,
                            'message': "You do not have access"
                        },
                        "results": []}, 403
            for funcion_permission in function.permissions:
                permission_list = Permissions.query.get(funcion_permission.id)
                access_level.append(permission_list.name)
            if user:
                for role_id in user.roles:
                    roles = Roles.query.get(role_id.id)
                    role.append(roles.name)
                    roles_permission.extend(roles.permissions)

                roles_permission.extend(user.permissions)
                permission_list = list(dict.fromkeys(roles_permission))
                for i in range(0, len(permission_list)):

                    permission_details = Permissions.query.get(
                        permission_list[i].id)
                    permissions.append(permission_details.name)

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
