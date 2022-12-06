import os

from pydantic import BaseSettings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
"""Корень проекта."""


class BaseTestConfig(BaseSettings):
    """Базовый класс для конфигураций, получающих значений из .env файла."""

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")


class TestSettings(BaseTestConfig):
    base_url: str = "/api/v1"
    """Базовый URL."""


test_settings = TestSettings()
