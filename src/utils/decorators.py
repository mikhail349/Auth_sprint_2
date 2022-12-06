from http import HTTPStatus
import functools

from flask_jwt_extended import verify_jwt_in_request, get_jwt

from src.api.v1.response_messages import NO_ACCESS


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
