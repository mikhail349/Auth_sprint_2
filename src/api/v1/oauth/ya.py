from src.core.config import yandex_oauth2_settings as settings
from src.api.v1.oauth.base import create_blueprint


def get_user_id(data):
    """Метод для получения уникального идентификатора пользователя."""
    return data["id"]


def get_email(data):
    """Метод для получения эл. почты."""
    return data['default_email']


def construct_info_request(token: str, **kwargs):
    """Метод для переопределения параметров запроса информации о пользователе.

    Args:
        token: токен доступа
        kwargs: опциональные параметры запроса (headers, params)

    """
    kwargs["headers"]["Authorization"] = "bearer {}".format(token)


ya = create_blueprint(
    social_name="yandex",
    url_prefix="/ya",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    auth_url=settings.auth_url,
    token_url=settings.token_url,
    base_url=settings.base_url,
    redirect_url=settings.redirect_url,
    get_user_id=get_user_id,
    get_email=get_email,
    construct_info_request=construct_info_request
)
"""Blueprint Yandex OAuth2."""
