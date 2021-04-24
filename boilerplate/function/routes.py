from .views.FunctionList import FunctionList
from .views.FunctionCreate import FunctionCreate
from .views.FunctionShow import FunctionShow
from .views.FunctionUpdate import FunctionUpdate
from .views.FunctionDelete import FunctionDelete


def initialize_routes(api):
    api.add_resource(FunctionList, '', methods=['GET'])
    api.add_resource(FunctionCreate, '', methods=['POST'])
    api.add_resource(FunctionUpdate, '/<int:id>', methods=['PUT'])
    api.add_resource(FunctionShow, '/<int:id>', methods=['GET'])
    api.add_resource(FunctionDelete, '/<int:id>', methods=['DELETE'])
