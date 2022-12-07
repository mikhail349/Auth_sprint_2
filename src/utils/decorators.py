from http import HTTPStatus
import functools

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

from src.api.v1.response_messages import NO_ACCESS, USER_DOESNT_EXIST
from src.models.user import User


def superuser_required():
    """Декоратор доступа суперпользователя."""
    def decorator(endpoint):
        @functools.wraps(endpoint)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('is_superuser'):
                return endpoint(*args, **kwargs)
            return NO_ACCESS, HTTPStatus.FORBIDDEN
        return wrapper
    return decorator


def user_required():
    """Декоратор доступа, который в endpoint передает инстанс user."""
    def decorator(endpoint):
        @functools.wraps(endpoint)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.query.filter_by(login=identity).one_or_none()
            if not user:
                return jsonify(USER_DOESNT_EXIST), HTTPStatus.BAD_REQUEST
            return endpoint(user=user, *args, **kwargs)
        return wrapper
    return decorator
