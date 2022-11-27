import json
from flask import current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, get_current_user
import datetime
from ..app import db, jwt
from .models import Transaction
from ..users.models import User
from ..utils.common import generate_response, get_reference
from .validation import CreatePaymentSchema
from ..utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from ..utils.decorator import admin_required


@jwt_required()
def create_payment(request, input_data):
    create_payment_validation_schema = CreatePaymentSchema()
    errors = create_payment_validation_schema.validate(input_data)
    current_user_name = get_jwt_identity()
    if errors:
        return generate_response(message=errors)

    if not current_user_name:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )

    user = User.query.filter_by(username=current_user_name).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    input_data['reference'] = get_reference()
    input_data['user_id'] = user.id
    new_payment = Transaction(**input_data)
    db.session.add(new_payment)
    db.session.commit()

    return generate_response(
            data=input_data, message="Transaction Created", status=HTTP_201_CREATED
        )


@admin_required()
def admin_create_payment(request, input_data, user_id):
    create_payment_validation_schema = CreatePaymentSchema()
    errors = create_payment_validation_schema.validate(input_data)
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return generate_response(
                message="User not found", status=HTTP_400_BAD_REQUEST
            )

    input_data['reference'] = get_reference()
    input_data['user_id'] = user.id
    new_payment = Transaction(**input_data)
    db.session.add(new_payment)
    db.session.commit()

    return generate_response(
            data=input_data, message="Transaction Created for user", status=HTTP_201_CREATED
        )
    


@admin_required()
def get_all_payments(request):
    payments = Transaction.query.all()

    if not payments:
        return generate_response(
                message="No transaction record", status=HTTP_404_NOT_FOUND
            )

    transaction_list = [payment.serialize() for payment in payments]


    return generate_response(
        data=transaction_list, message="transactions fetched", status=HTTP_200_OK
    )

@admin_required()
def get_all_customer_payments(request, user_id):
    payments = Transaction.query.filter_by(user_id=user_id).all()

    if not payments:
        return generate_response(
                message="No transaction record", status=HTTP_400_BAD_REQUEST
            )

    transaction_list = [payment.serialize() for payment in payments]


    return generate_response(
        data=transaction_list, message="user transactions fetched", status=HTTP_200_OK
    )


@admin_required()
def get_single_customer_payments(request, user_id, reference):
    payments = Transaction.query.filter_by(user_id=user_id, reference=reference).first()

    if not payments:
        return generate_response(
                message="No transaction record", status=HTTP_400_BAD_REQUEST
            )

    return generate_response(
        data=payments.serialize(), message="user transactions fetched", status=HTTP_200_OK
    )

@jwt_required()
def get_all_user_payments(request):

    current_user_name = get_jwt_identity()

    if not current_user_name:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )

    user = User.query.filter_by(username=current_user_name).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    payments = Transaction.query.filter_by(user_id=user.id).all()

    if not payments:
        return generate_response(
                message="No transaction record", status=HTTP_404_NOT_FOUND
            )

    transaction_list = [payment.serialize() for payment in payments]


    return generate_response(
        data=transaction_list, message="user transactions fetched", status=HTTP_200_OK
    )


@jwt_required()
def get_customer_single_payment(request, reference):
    transaction = Transaction.query.filter_by(reference=reference).first()

    if not transaction:
        return generate_response(
                message="No transaction record", status=HTTP_404_NOT_FOUND
            )

    current_user_name = get_jwt_identity()

    if not current_user_name:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )

    user = User.query.filter_by(username=current_user_name).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    if user.id != transaction.user_id:
        return generate_response(
                message="can only fecth own transaction", status=HTTP_400_BAD_REQUEST
            )

    return generate_response(
        data=transaction.serialize(), message="user transactions fetched", status=HTTP_200_OK
    )


@admin_required()
def get_single_payment(request, reference):
    transaction = Transaction.query.filter_by(reference=reference).first()

    if not transaction:
        return generate_response(
                message="No transaction record", status=HTTP_404_NOT_FOUND
            )

    current_user_name = get_jwt_identity()


    return generate_response(
        data=transaction.serialize(), message="user transactions fetched", status=HTTP_200_OK
    )