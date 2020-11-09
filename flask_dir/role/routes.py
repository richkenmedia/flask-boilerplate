from .views.RoleList import RoleList
from .views.RoleCreate import RoleCreate
from .views.RoleShow import RoleShow
from .views.RoleUpdate import RoleUpdate
from .views.RoleDelete import RoleDelete


def initialize_routes(api):
    api.add_resource(RoleList, '', methods=['GET'])
    api.add_resource(RoleCreate, '', methods=['POST'])
    api.add_resource(RoleUpdate, '/<int:id>', methods=['PUT'])
    api.add_resource(RoleShow, '/<int:id>', methods=['GET'])
    api.add_resource(RoleDelete, '/<int:id>', methods=['DELETE'])
