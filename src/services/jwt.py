from flask import Flask

from src.app.extensions import jwt
from src.core.config import jwt_settings


def init_jwt(app: Flask):
    """Инициализировать модуль JWT.

    Args:
        app: приложение Flask

    """
    app.config.from_mapping(jwt_settings.uppercased_dict())
    app.config['JWT_PRIVATE_KEY'] = open(jwt_settings.jwt_private_key_path).read()
    app.config['JWT_PUBLIC_KEY'] = open(jwt_settings.jwt_public_key_path).read()
    jwt.init_app(app)
