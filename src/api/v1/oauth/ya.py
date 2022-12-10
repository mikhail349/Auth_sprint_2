from src.core.config import yandex_oauth2_settings as settings
from src.api.v1.oauth.base import create_blueprint


def get_id(data):
    """Метод для получения уникального идентификатора пользователя."""
    return data["id"]


ya = create_blueprint(
    social_name="yandex",
    url_prefix="/ya",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    auth_url=settings.auth_url,
    token_url=settings.token_url,
    base_url=settings.base_url,
    redirect_url=settings.redirect_url,
    get_id=get_id
)
"""Blueprint Yandex OAuth2."""
