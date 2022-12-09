import functools
from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from opentelemetry import trace as ot_trace

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


def user_required(*jwt_args, **jwt_kwargs):
    """Декоратор доступа, который в endpoint передает инстанс user."""
    def decorator(endpoint):
        @functools.wraps(endpoint)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(*jwt_args, **jwt_kwargs)
            identity = get_jwt_identity()
            user = User.query.filter_by(login=identity).one_or_none()
            if not user:
                return jsonify(USER_DOESNT_EXIST), HTTPStatus.BAD_REQUEST
            return endpoint(user=user, *args, **kwargs)
        return wrapper
    return decorator


def trace(func):
    """Декоратор для трассировок любых функций."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request_id = request.headers.get('X-Request-Id')
        tracer = ot_trace.get_tracer(__name__)
        span = tracer.start_span(func.__name__)
        span.set_attribute('http.request_id', request_id)
        span.end()
        return func(*args, **kwargs)
    return wrapper
