from http import HTTPStatus

import pytest
from werkzeug.test import TestResponse

from src.models.user import User
from src.services.user import UserService
from tests.functional.const import auth
from tests.functional.const.api import user as api
from tests.functional.const.response_messages import user as msg
from tests.functional.src.base import TestBase


class TestUser(TestBase):
    """Базовый Класс тестирования /user endpoint."""

    @property
    def url(self):
        _url = super().url
        return f'{_url}{api.BASE_URL}'

    def login(self, body: str) -> TestResponse:
        """Функция логина.

        Args:
            body: тело запроса

        Returns:
            TestResponse: ответ на запрос

        """
        return self.client.post(f'{self.url}{api.LOGIN}', json=body)

    def logout(self, headers: dict) -> TestResponse:
        """Функция логаута.

        Args:
            headers: заголовки запроса

        Returns:
            TestResponse: ответ на запрос

        """
        return self.client.post(f'{self.url}{api.LOGOUT}', headers=headers)

    def refresh_token(self, token: str) -> TestResponse:
        """Функция обновления токена доступа.

        Args:
            token: токен

        Returns:
            TestResponse: ответ на запрос

        """
        return self.client.post(f'{self.url}{api.REFRESH_TOKEN}', headers=self.get_auth_header(token))

    @pytest.mark.parametrize(
        "body, expected_response",
        [
            (
                {"username": "new_user", "password": "123"},
                {"status_code": HTTPStatus.OK, "json": msg.USER_CREATED}
            ),
            (
                {"username": "new_user"},
                {"status_code": HTTPStatus.BAD_REQUEST, "json": msg.WRONG_INPUT}
            ),
            (
                {"username": auth.LOGIN, "password": auth.PASSWORD},
                {"status_code": HTTPStatus.BAD_REQUEST, "json": msg.USER_EXISTS}
            ),
        ],
        ids=["correct data",
             "no password",
             "duplicated user"]
    )
    def test_register(self, user, body, expected_response):
        """Тест регистрации."""
        response = self.client.post(f'{self.url}{api.REGISTER}', json=body)
        try:
            self.assert_response(response, expected_response)
        finally:
            if response.status_code == HTTPStatus.OK:
                created_user = User.query.filter_by(login=body['username']).one_or_none()
                if created_user:
                    UserService.delete(created_user)

    @pytest.mark.parametrize(
        "body, expected_response",
        [
            (
                {"username": auth.LOGIN, "password": auth.PASSWORD},
                {"status_code": HTTPStatus.OK}
            ),
            (
                {"username": auth.LOGIN, "password": "1234"},
                {"status_code": HTTPStatus.UNAUTHORIZED}
            ),
            (
                {"username": "qwerty", "password": auth.PASSWORD},
                {"status_code": HTTPStatus.UNAUTHORIZED}
            ),
        ],
        ids=["existent user with correct password",
             "existent user with wrong password",
             "nonexistent user"]
    )
    def test_login(self, user, body, expected_response):
        """Тест логина."""
        response = self.login(body)
        self.assert_response(response, expected_response)

    @pytest.mark.parametrize(
        "expected_response",
        [
            (
                {"status_code": HTTPStatus.OK, "json": msg.LOGGED_OUT}
            ),
        ]
    )
    def test_logout(self, auth_headers, expected_response):
        """Тест логаута."""
        response = self.logout(auth_headers)
        self.assert_response(response, expected_response)

    @pytest.mark.parametrize(
        "body, expected_response",
        [
            (
                {"username": "new_login", "password": "new_password"},
                {"username": "new_login", "status_code": HTTPStatus.OK}
            ),
            (
                {"username": "new_user"},
                {"username": "user", "status_code": HTTPStatus.BAD_REQUEST, "json": msg.WRONG_INPUT}
            ),
        ],
        ids=["correct data",
             "no password"]
    )
    def test_update(self, client, auth, auth_headers, body, expected_response):
        """Тест изменения данных пользователя."""
        response = self.client.put(f'{self.url}{api.UPDATE}', headers=auth_headers, json=body)
        self.assert_response(response, expected_response)
        assert auth['user'].login == expected_response['username']

    @pytest.mark.parametrize(
        "params, expected_response",
        [
            (
                {'token_name': 'refresh_token'},
                {"status_code": HTTPStatus.OK}
            ),
            (
                {'token_name': 'access_token'},
                {"status_code": HTTPStatus.UNPROCESSABLE_ENTITY, "json": msg.REFRESH_TOKEN_REQUIRED}
            )
        ],
        ids=["refresh by refresh-token",
             "refresh by access-token"]
    )
    def test_refresh_token(self, auth, params, expected_response):
        """Тест обновления access токена."""
        response = self.refresh_token(auth[params['token_name']])
        self.assert_response(response, expected_response)

    @pytest.mark.parametrize(
        "expected_response",
        [
            (
                {"status_code": HTTPStatus.UNAUTHORIZED, "json": msg.REVOKED_TOKEN}
            ),
        ]
    )
    def test_refresh_revoked_token(self, auth, auth_headers, expected_response):
        """Тест обновления уже отозванного access токена."""
        self.logout(auth_headers)
        response = self.refresh_token(auth['refresh_token'])
        self.assert_response(response, expected_response)

    @pytest.mark.parametrize(
        "body, query, expected_response",
        [
            (
                    {"username": auth.LOGIN, "password": auth.PASSWORD},
                    None,
                    {"status_code": HTTPStatus.OK, "json_len": 3},
            ),
            (
                    {"username": auth.LOGIN, "password": auth.PASSWORD},
                    {"page": 2, "size": 2},
                    {"status_code": HTTPStatus.OK, "json_len": 1},
            ),
            (
                    {"username": auth.LOGIN, "password": auth.PASSWORD},
                    {"page": -1, "size": -1},
                    {"status_code": HTTPStatus.NOT_FOUND},
            ),
        ],
    )
    def test_auth_history(self, user, body, expected_response, query):
        """Тест получения истории входов в аккаунт."""
        for _ in range(3):
            response = self.login(body)

        response = self.client.get(
            f"{self.url}{api.LOGIN_HISTORY}",
            headers=self.get_auth_header(response.json["access_token"]),
            query_string=query
        )
        self.assert_response(response, expected_response)

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_update_role(self, user, auth_headers, role):
        """Проверка обновления ролей у пользователя."""
        response = self.client.post(
            f"{self.url}/{user.id}/roles/{role.name}", headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.OK,
                                        "json": msg.ROLE_UPDATED})
        response = self.client.delete(
            f"{self.url}/{user.id}/roles/{role.name}", headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.OK,
                                        "json": msg.ROLE_DELETED})
