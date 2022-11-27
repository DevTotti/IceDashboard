import json
from flask import current_app, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, set_access_cookies, get_jwt, unset_jwt_cookies, verify_jwt_in_request, get_jwt_identity, set_refresh_cookies
import datetime
from ..app import db, jwt
from .models import User, Role, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.common import generate_response
from .validation import (
    CreateLoginInputSchema,
    CreateSignupInputSchema, ResetPasswordInputSchema,
    UpdateCustomerInputSchema
)
from ..utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from ..utils.decorator import admin_required


def create_user(request, input_data):

    create_validation_schema = CreateSignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_username_exist = User.query.filter_by(
        username=input_data.get("username")
    ).first()
    check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
    if check_username_exist:
        return generate_response(
            message="Username already exist", status=HTTP_400_BAD_REQUEST
        )
    elif check_email_exist:
        return generate_response(
            message="Email  already taken", status=HTTP_400_BAD_REQUEST
        )
    new_user = User(**input_data)  # Create an instance of the User class
    new_user.set_password(input_data.get('password'))
    db.session.add(new_user)  # Adds new User record to database
    db.session.commit()  # Commint
    del input_data["password"]
    if input_data.get("email").endswith('@iceadmin.net'):
        admin = Role.query.filter_by(name='admin').first()
        admin_data = {
            "user_id": new_user.id,
            "user_role_id": admin.id
        }
        new_admin = UserRole(**admin_data)
        db.session.add(new_admin)
        db.session.commit()
        
    return generate_response(
        data=input_data, message="User Created", status=HTTP_201_CREATED
    )


def login_user(request, input_data):
    create_validation_schema = CreateLoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    get_user = User.query.filter_by(email=input_data.get("email")).first()
    if get_user is None:
        return generate_response(message="User not found", status=HTTP_400_BAD_REQUEST)
    if get_user.check_password(input_data.get("password")):
        token = create_access_token(
            identity=get_user.username, 
            additional_claims={
                "id": get_user.id, 
                "email": get_user.email
            }
        )
        refresh_token = create_refresh_token(identity=get_user.username)
        input_data["token"] = token
        response = jsonify({'message': 'login successful'})
        set_access_cookies(response, token)
        set_refresh_cookies(response, refresh_token)
        return generate_response(
            data=input_data, message="User login successfully", status=HTTP_201_CREATED
        )
    else:
        return generate_response(
            message="Password is wrong", status=HTTP_400_BAD_REQUEST
        )


@jwt_required()
def reset_password(request, input_data):
    create_validation_schema = ResetPasswordInputSchema()
    errors = create_validation_schema.validate(input_data)
    current_user_name = get_jwt_identity()
    if errors:
        return generate_response(message=errors)
    if not current_user_name:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )
    user = User.query.filter_by(username=current_user_name).first()
    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    user.password = generate_password_hash(input_data.get('password'))
    db.session.commit()
    return generate_response(
        message="New password SuccessFully set.", status=HTTP_200_OK
    )


@jwt_required()
def user_update(request, input_data):

    update_validation_schema = UpdateCustomerInputSchema()
    errors = update_validation_schema.validate(input_data)

    if errors:
        return generate_response(message=errors)

    current_user_name = get_jwt_identity()
    user = User.query.filter_by(username=current_user_name).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    if input_data.get('email'):
        check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
        if check_email_exist:
            return generate_response(
                message="Email  already taken", status=HTTP_400_BAD_REQUEST
            )
        user.email = input_data.get("email")
    
    if input_data.get('username'):
        check_username_exist = User.query.filter_by(username=input_data.get("username")).first()
        if check_username_exist:
            return generate_response(
                message="Username already exist", status=HTTP_400_BAD_REQUEST
            )
        user.username = input_data.get('username')

    db.session.commit()  # Commit
    return generate_response(
        data=input_data, message="User Record Updated", status=HTTP_201_CREATED
    )


@admin_required()
def delete_customer(request, user_id):

    user = User.query.filter_by(id=user_id).one()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    db.session.delete(user)
    db.session.commit()
    return generate_response(
        data=user_id, message="User Record deleted", status=HTTP_200_OK
    )


@admin_required()
def fetch_customer(request, user_id):

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    return generate_response(
        data=user.serialize(), message="User Record fetched", status=HTTP_200_OK
    )

@admin_required()
def fetch_all_customer(request):

    users = User.query.all()

    if not users:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    user_list = [user.serialize() for user in users]

    return generate_response(
        data=user_list, message="User Record fetched", status=HTTP_200_OK
    )


@jwt_required()
def get_profile(request):

    current_user_name = get_jwt_identity()
    user = User.query.filter_by(username=current_user_name).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    return generate_response(
        data=user.serialize(), message="User Record fetched", status=HTTP_200_OK
    )


@admin_required()
def update_customer(request, input_data, user_id):

    update_validation_schema = UpdateCustomerInputSchema()
    errors = update_validation_schema.validate(input_data)

    if errors:
        return generate_response(message=errors)

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return generate_response(
                message="User record does not exist", status=HTTP_400_BAD_REQUEST
            )

    if input_data.get('email'):
        check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
        if check_email_exist:
            return generate_response(
                message="Email  already taken", status=HTTP_400_BAD_REQUEST
            )
        user.email = input_data.get("email")
    
    if input_data.get('username'):
        check_username_exist = User.query.filter_by(username=input_data.get("username")).first()
        if check_username_exist:
            return generate_response(
                message="Username already exist", status=HTTP_400_BAD_REQUEST
            )
        user.username = input_data.get('username')

    db.session.commit()  # Commit
    return generate_response(
        data=input_data, message="User Record Updated", status=HTTP_201_CREATED
    )