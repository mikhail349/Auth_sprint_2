from src.core.config import google_oauth2_settings as settings
from src.api.v1.oauth.base import create_blueprint


def get_user_id(data):
    """Метод для получения уникального идентификатора пользователя."""
    return data["sub"]


def construct_info_request(token: str, headers: dict, **_):
    """Метод для переопределения параметров запроса авторизации.

    Args:
        data: тело запроса

    """
    data["redirect_uri"] = settings.redirect_url


def construct_info_request(token: str, params: dict, **_):
    """Метод для переопределения параметров запроса информации о пользователе.

    Args:
        token: токен доступа
        kwargs: опциональные параметры запроса (headers, params)

    """
    kwargs["params"]["access_token"] = token


google = create_blueprint(
    social_name="google",
    url_prefix="/google",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    auth_url=settings.auth_url,
    token_url=settings.token_url,
    base_url=settings.base_url,
    redirect_url=settings.redirect_url,
    get_user_id=get_user_id,
    construct_auth_request=construct_auth_request,
    construct_info_request=construct_info_request
)
"""Blueprint Google OAuth2."""
