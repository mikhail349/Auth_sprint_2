import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
"""Корень проекта."""


class BaseConfig(BaseSettings):
    """Базовый класс для конфигураций, получающих значений из .env файла."""

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")

    def uppercased_dict(self):
        """Получить параметры настройки в виде словаря с UPPER_CASE ключами"""
        return {k.upper(): v for k, v in self.dict().items()}


class PostgresSettings(BaseConfig):
    """Настройки для подключения к базе данных PostgreSQL."""

    postgres_db: str = "db_name"
    """Название базы данных для подключения к PostgreSQL."""
    postgres_user: str = "user"
    """Имя пользователя для подключения к PostgreSQL."""
    postgres_password: str = "pass"
    """Пароль для подключения к PostgreSQL."""
    db_host: str = "0.0.0.0"
    """HOST для подключения к PostgreSQL."""
    db_port: int = 5432
    """Порт для подключения к PostgreSQL."""


class RedisSettings(BaseConfig):
    """Настройки для подключения к Redis."""

    redis_host: str = "127.0.0.1"
    """Host для подключения к Redis."""
    redis_port: int = 6379
    """Порт для подключения к Redis."""
    redis_db_tokens_revoked: int = 0
    """Номер базы данных для хранения токенов в Redis."""
    redis_db_tokens_access_refresh_map: int = 1
    """Номер базы данных для хранения маппинга access/refresh в Redis."""


class JWTSettings(BaseConfig):
    jwt_token_location: list[str] = ["headers"]
    jwt_secret_key: str = Field("super-secret", env='JWT_SECRET_KEY')
    jwt_access_token_expires: int = Field(3600, env='JWT_ACCESS_TOKEN_EXPIRES')
    jwt_refresh_token_expires: int = Field(864000, env='JWT_REFRESH_TOKEN_EXPIRES')


class YandexOAuth2Settings(BaseConfig):
    """Настройки для работы с Яндекс OAuth2."""
    client_id: str = Field(None, env="YANDEX_OAUTH2_CLIENT_ID")
    """ИД клиента."""
    client_secret: str = Field(None, env="YANDEX_OAUTH2_CLIENT_SECRET")
    """Секрет клиента."""
    auth_url: str = Field("https://oauth.yandex.ru/authorize", env="YANDEX_OAUTH2_AUTH_URL")
    """URL получения кода."""
    token_url: str = Field("https://oauth.yandex.ru/token", env="YANDEX_OAUTH2_TOKEN_URL")
    """URL получения токена."""
    base_url: str = Field("https://login.yandex.ru/info", env="YANDEX_OAUTH2_BASE_URL")
    """URL получения информации из Яндекс API."""
    redirect_url: str = Field("https://<auth_service>/api/v1/oauth/ya/tokens", env="YANDEX_OAUTH2_REDIRECT_URL")
    """URL для callback, куда будет передан код авторизации."""


class AppSettings(BaseConfig):
    default_page: int = 1
    """Номер страницы по умолчанию."""
    default_page_size: int = 10
    """Размер страницы по умолчанию."""


postgres_settings = PostgresSettings()
redis_settings = RedisSettings()
jwt_settings = JWTSettings()
app_settings = AppSettings()
yandex_oauth2_settings = YandexOAuth2Settings()
