from .views.ForgotPassword import ForgotPassword
from .views.ResetPassword import ResetPassword


def initialize_routes(api):
    api.add_resource(ForgotPassword, 'forgot-password')
    api.add_resource(ResetPassword, 'reset-password')
