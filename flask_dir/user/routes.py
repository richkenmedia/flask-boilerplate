from .views import User, UserWithParameter, ChangePassword


def initialize_routes(api):
    api.add_resource(User, '')
    api.add_resource(UserWithParameter, '<string:id>')
    api.add_resource(ChangePassword, '/change-password')
