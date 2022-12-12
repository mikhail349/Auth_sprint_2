from src.core.config import google_oauth2_settings as settings
from src.api.v1.oauth.base import create_blueprint


def get_id(data):
    """Метод для получения уникального идентификатора пользователя."""
    return data["sub"]


google = create_blueprint(
    social_name="google",
    url_prefix="/google",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    auth_url=settings.auth_url,
    token_url=settings.token_url,
    base_url=settings.base_url,
    redirect_url=settings.redirect_url,
    get_id=get_id
)
"""Blueprint Google OAuth2."""
