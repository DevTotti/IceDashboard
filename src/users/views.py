from flask import Response
from flask_restful import Resource
from flask import request, make_response
from .service import create_user, login_user, reset_password, user_update, update_customer, delete_customer, fetch_customer, get_profile, fetch_all_customer


class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for login user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)


class ResetPassword(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for save new password.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = reset_password(request, input_data)
        return make_response(response, status)


class AdminUpdateCustomer(Resource):
    @staticmethod
    def put(user_id) -> Response:
        input_data = request.get_json()
        response, status = update_customer(request, input_data, user_id)
        return make_response(response, status)


class AdminDeleteCustomer(Resource):
    @staticmethod
    def delete(user_id) -> Response:
        response, status = delete_customer(request, user_id)
        return make_response(response, status)


class AdminFetchCustomer(Resource):
    @staticmethod
    def get(user_id) -> Response:
        response, status = fetch_customer(request, user_id)
        return make_response(response, status)


class AdminFetchCustomers(Resource):
    @staticmethod
    def get() -> Response:
        response, status = fetch_all_customer(request)
        return make_response(response, status)


class GetProfile(Resource):
    @staticmethod
    def get() -> Response:
        response, status = get_profile(request)
        return make_response(response, status)


class UpdateAccount(Resource):
    @staticmethod
    def put() -> Response:
        input_data = request.get_json()
        response, status = user_update(request, input_data)
        return make_response(response, status)