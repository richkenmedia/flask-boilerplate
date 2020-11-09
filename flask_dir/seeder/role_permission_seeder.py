import os

from dotenv import load_dotenv

from flask_dir import create_app
from flask_dir import db
from flask_dir.permission.models import Permissions
from flask_dir.role.models import Roles


project_folder = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))  # Path to .env file
load_dotenv(os.path.join(project_folder, '.env'))
app = create_app()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')


class RolePermissionSeeder:
    def roleseeder():
        try:

            with app.app_context():
                roles = Roles.query.all()
                if len(roles) == 0:
                    permission_list = [
                        Permissions(name="admin_list", status="active"),
                        Permissions(name="admin_create", status="active"),
                        Permissions(name="admin_show", status="active"),
                        Permissions(name="admin_update", status="active"),
                        Permissions(name="admin_delete", status="active"),
                        Permissions(name="admin_report", status="active"),

                    ]
                    db.session.bulk_save_objects(
                        permission_list, return_defaults=True)
                    db.session.commit()
                    role = Roles(name='admin', status="active")
                    role.permissions.extend(permission_list)
                    db.session.add(role)
                    db.session.commit()

                    permission_list = [
                        Permissions(name="user_list", status="active"),
                        Permissions(name="user_create", status="active"),
                        Permissions(name="user_show", status="active"),
                        Permissions(name="user_update", status="active"),
                        Permissions(name="user_delete", status="active"),
                        Permissions(name="user_report", status="active"),

                    ]
                    db.session.bulk_save_objects(
                        permission_list, return_defaults=True)
                    db.session.commit()
                    role = Roles(name='user', status="active")
                    role.permissions.extend(permission_list)
                    db.session.add(role)
                    db.session.commit()
                    print("Role Permission Seeder Executed Successfully")
                else:
                    print("Role Permission Seeder Already Executed")
        except Exception as e:
            print("Some Error Occurs: ", e)
