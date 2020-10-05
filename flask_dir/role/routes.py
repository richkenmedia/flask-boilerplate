from .views import Role, RoleWithParameter


def initialize_routes(api):
    api.add_resource(Role, '')
    api.add_resource(RoleWithParameter, '/<string:id>')
