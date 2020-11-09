import sys


def seeder():
    from flask_dir.seeder.role_permission_seeder import RolePermissionSeeder
    RolePermissionSeeder.roleseeder()


if __name__ == "__main__":
    globals()[sys.argv[1]]()
