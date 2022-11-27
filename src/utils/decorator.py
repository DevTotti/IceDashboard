from ..users.models import User, Role, UserRole
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from .common import generate_response
from functools import wraps
from flask import jsonify


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_name = get_jwt_identity()
            if not current_user_name:
                return generate_response(
                    message="Invalid user!",
                    status=HTTP_400_BAD_REQUEST,
                )

            user = User.query.filter_by(username=current_user_name).first()
            admin = Role.query.filter_by(name='admin').first()
            query_user_role = User.query.join(UserRole).join(Role).filter((UserRole.user_id == user.id) & (UserRole.user_role_id == admin.id)).all()
            if query_user_role:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper