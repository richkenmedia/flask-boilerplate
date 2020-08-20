
import datetime
from flask_dir import mongo


def create_permission_role(permission_id, name):

    role = mongo.db.roles.insert_one({
        "name": name,
        "description": "",
        'status': "active",
        "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "permissions": permission_id,
        "updated_at": "",
        "created_by": "",
        "updated_by": "",
    })

    for i in range(0, len(permission_id)):
        mongo.db.permissions.update_one(
            {'_id': permission_id[i]},
            {
                "$set": {
                    "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                },
                "$addToSet": {
                    "roles": role.inserted_id
                }
            }
        )
    return True


class RolePermissionSeeder:
    try:
        permissions = mongo.db.permissions.count()
        roles = mongo.db.roles.count()
        if permissions == 0 and roles == 0:
            user = [
                {
                    "name": 'user_create',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'user_update',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'user_show',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'user_delete',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'user_list',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'user_report',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                }

            ]

            user_permission_id = mongo.db.permissions.insert_many(user)
            create_permission_role(
                user_permission_id.inserted_ids, 'user')

            admin = [
                {
                    "name": 'admin_create',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'admin_update',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'admin_show',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'admin_delete',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'admin_list',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'admin_report',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                }

            ]
            admin_permission_id = mongo.db.permissions.insert_many(admin)
            create_permission_role(admin_permission_id.inserted_ids, 'admin')

    except Exception as e:
        pass
