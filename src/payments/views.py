from flask import Response
from flask_restful import Resource
from flask import request, make_response
from .service import (
    create_payment,
    admin_create_payment,
    get_all_payments,
    get_all_customer_payments,
    get_single_customer_payments,
    get_all_user_payments,
    get_customer_single_payment,
    get_single_payment
    )


class CustomerPayment(Resource):
    @staticmethod
    def post() -> Response:
        input_data = request.get_json()
        response, status = create_payment(request, input_data)
        return make_response(response, status)


class AdminCreatePayment(Resource):
    @staticmethod
    def post(user_id) -> Response:
        input_data = request.get_json()
        response, status = admin_create_payment(request, input_data, user_id)
        return make_response(response, status)


class AdminGetAllPayments(Resource):
    @staticmethod
    def get() -> Response:
        response, status = get_all_payments(request)
        return make_response(response, status)


class AdminGetAllCustomerPayments(Resource):
    @staticmethod
    def get(user_id) -> Response:
        response, status = get_all_customer_payments(request, user_id)
        return make_response(response, status)


class AdminGetSinglePayment(Resource):
    @staticmethod
    def get(reference) -> Response:
        response, status = get_single_payment(request, reference)
        return make_response(response, status)

class AdminGetCustomerSinglePayment(Resource):
    @staticmethod
    def get(user_id, reference) -> Response:
        response, status = get_single_customer_payments(request, user_id, reference)
        return make_response(response, status)

class CustomerSinglePayment(Resource):
    @staticmethod
    def get(reference) -> Response:
        response, status = get_customer_single_payment(request, reference)
        return make_response(response, status)

class CustomerGetAllPayment(Resource):
    @staticmethod
    def get() -> Response:
        response, status = get_all_user_payments(request)
        return make_response(response, status)