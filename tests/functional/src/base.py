import pytest

from tests.functional.settings import test_settings


@pytest.mark.usefixtures("client")
class TestBase:
    """Базовый класс для тестов."""

    @property
    def url(self):
        """Базовый url."""
        return test_settings.base_url

    def get_auth_header(self, token: str) -> dict:
        """Получить заголовки запроса с авторизацией.

        Args:
            token: токен

        Returns:
            dict: заголовки запроса

        """
        return {
            'Authorization': 'Bearer {}'.format(token)
        }

    def assert_response(self, response, expected_response):
        """Выполнить проверку.

        Args:
            response: ответ сервиса
            expected_response: ожидаемый ответ сервиса

        """
        if 'status_code' in expected_response:
            assert response.status_code == expected_response['status_code']
        if 'json' in expected_response:
            assert response.json == expected_response['json'], response.json
        if 'json_len' in expected_response:
            assert len(response.json) == expected_response['json_len'], response.json
