from .views.PermissionList import PermissionList
from .views.PermissionCreate import PermissionCreate
from .views.PermissionShow import PermissionShow
from .views.PermissionUpdate import PermissionUpdate
from .views.PermissionDelete import PermissionDelete


def initialize_routes(api):
    api.add_resource(PermissionList, '', methods=['GET'])
    api.add_resource(PermissionCreate, '', methods=['POST'])
    api.add_resource(PermissionUpdate, '/<int:id>', methods=['PUT'])
    api.add_resource(PermissionShow, '/<int:id>', methods=['GET'])
    api.add_resource(PermissionDelete, '/<int:id>', methods=['DELETE'])
