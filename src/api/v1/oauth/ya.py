from src.core.config import yandex_oauth2_settings as settings
from src.api.v1.oauth.base import create_blueprint


ya = create_blueprint(
    social_name="yandex",
    url_prefix="/ya",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    token_url=settings.token_url,
    base_url=settings.base_url
)
"""Blueprint Yandex OAuth2."""
