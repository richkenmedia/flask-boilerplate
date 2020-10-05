from .views import Permission, PermissionWithParameter


def initialize_routes(api):
    api.add_resource(Permission, '')
    api.add_resource(PermissionWithParameter, '/<string:id>')
