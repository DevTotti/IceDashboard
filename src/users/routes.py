from flask_restful import Api
from .views import LoginApi, SignUpApi, ResetPassword, AdminUpdateCustomer, UpdateAccount, GetProfile, AdminFetchCustomer, AdminDeleteCustomer, AdminFetchCustomers


def create_authentication_routes(api: Api):
    """Adds resources to the api.
    :param api: Flask-RESTful Api Object
    """
    api.add_resource(SignUpApi, "/api/auth/register/")
    api.add_resource(LoginApi, "/api/auth/login/")
    api.add_resource(ResetPassword, "/api/auth/reset-password/")
    api.add_resource(UpdateAccount, "/api/profile/update-account/")
    api.add_resource(GetProfile, "/api/profile/")
    api.add_resource(AdminUpdateCustomer, "/api/admin/update-customer/<user_id>")
    api.add_resource(AdminDeleteCustomer, "/api/admin/delete-customer/<user_id>")
    api.add_resource(AdminFetchCustomer, "/api/admin/get-customer/<user_id>")
    api.add_resource(AdminFetchCustomers, "/api/admin/get-all-customers")