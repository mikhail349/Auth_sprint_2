from dataclasses import asdict
from http import HTTPStatus

import pytest

from tests.functional.const.api import role as role_api
from tests.functional.src.base import TestBase
from tests.functional.src.lib.models.role import Role


class TestRole(TestBase):
    """Класс тестирования /roles endpoint."""

    @property
    def url(self):
        _url = super().url
        return f'{_url}{role_api.BASE_URL}'

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_list_view(self, user, auth_headers, role):
        """Тест получения списка ролей."""
        response = self.client.get(self.url, headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.OK})

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_detailed_view(self, user, auth_headers, role):
        """Тест получения информации о роли по id."""
        response = self.client.get(f"{self.url}/{role.id}", headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        assert Role(**response.json) == role

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_creation(self, user, auth_headers, role_data):
        """Тест на создание роли."""
        response = self.client.post(
            self.url, headers=auth_headers, json=asdict(role_data)
        )
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        assert response.json["name"] == role_data.name

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_update(self, user, auth_headers, role):
        """Тест на изменение роли."""
        role.name = "upd_" + role.name
        response = self.client.put(
            f"{self.url}/{role.id}",
            headers=auth_headers,
            json=asdict(role),
        )
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        assert response.json["name"] == role.name

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_delete(self, user, auth_headers, role):
        """Тест на удаление роли."""
        response = self.client.delete(
            f"{self.url}/{role.id}", headers=auth_headers
        )
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        response = self.client.get(f"{self.url}/{role.id}", headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.NOT_FOUND})
