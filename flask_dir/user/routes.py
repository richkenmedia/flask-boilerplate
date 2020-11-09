from .views.UserList import UserList
from .views.UserUpdate import UserUpdate
from .views.UserShow import UserShow
from .views.UserDelete import UserDelete
from .views.ChangePassword import ChangePassword


def initialize_routes(api):
    api.add_resource(UserList, '')
    api.add_resource(UserUpdate, '<int:id>', methods=['PUT'])
    api.add_resource(UserShow, '<int:id>', methods=['GET'])
    api.add_resource(UserDelete, '<int:id>', methods=['DELETE'])
    api.add_resource(ChangePassword, 'change-password')
