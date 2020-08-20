
import datetime
from skill_tracker import mongo


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
            employee = [
                {
                    "name": 'employee_create',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'employee_update',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'employee_show',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'employee_delete',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'employee_list',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'employee_report',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                }

            ]

            employee_permission_id = mongo.db.permissions.insert_many(employee)
            create_permission_role(
                employee_permission_id.inserted_ids, 'employee')

            tenant = [
                {
                    "name": 'tenant_create',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'tenant_update',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'tenant_show',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'tenant_delete',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'tenant_list',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                },
                {
                    "name": 'tenant_report',
                    'status': 'active',
                    "created_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at": "",
                    "created_by": "",
                    "updated_by": "",
                }

            ]
            tenant_permission_id = mongo.db.permissions.insert_many(tenant)
            create_permission_role(tenant_permission_id.inserted_ids, 'tenant')

    except Exception as e:
        pass
