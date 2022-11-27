from flask_restful import Api
from .views import (
    CustomerPayment,
    AdminCreatePayment,
    AdminGetAllPayments,
    AdminGetAllCustomerPayments,
    AdminGetSinglePayment,
    AdminGetCustomerSinglePayment,
    CustomerSinglePayment,
    CustomerGetAllPayment
    )

def create_payment_routes(api: Api):

    api.add_resource(CustomerPayment, "/api/payment/create")
    api.add_resource(AdminCreatePayment, "/api/admin/payments/create/<user_id>")
    api.add_resource(AdminGetAllPayments, "/api/admin/payments/")
    api.add_resource(AdminGetAllCustomerPayments, "/api/admin/payment-user/<user_id>")
    api.add_resource(AdminGetSinglePayment, "/api/admin/payment-ref/<reference>")
    api.add_resource(AdminGetCustomerSinglePayment, "/api/admin/payment-ref-user/<user_id>/<reference>")
    api.add_resource(CustomerSinglePayment, "/api/payment/<reference>")
    api.add_resource(CustomerGetAllPayment, "/api/payments/")