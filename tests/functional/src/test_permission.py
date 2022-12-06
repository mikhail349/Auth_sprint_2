from dataclasses import asdict
from http import HTTPStatus

import pytest

from tests.functional.const.api import permission as perm_api
from tests.functional.src.base import TestBase
from tests.functional.src.lib.models.permission import Permission


class TestPermission(TestBase):
    """Класс тестирования /perms endpoint."""

    @property
    def url(self):
        _url = super().url
        return f'{_url}{perm_api.BASE_URL}'

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_list_view(self, user, auth_headers, permission):
        """Тест получения списка прав."""
        response = self.client.get(self.url, headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.OK})

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_detailed_view(self, user, auth_headers, permission):
        """Тест получения информации о праве по id."""
        response = self.client.get(f"{self.url}/{permission.id}", headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        assert Permission(**response.json) == permission

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_creation(self, user, auth_headers, permission_data):
        """Тест на создание права."""
        response = self.client.post(
            self.url, headers=auth_headers, json=asdict(permission_data)
        )
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        assert response.json["name"] == permission_data.name

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_update(self, user, auth_headers, permission):
        """Тест на изменение права."""
        permission.name = "upd_" + permission.name
        response = self.client.put(
            f"{self.url}/{permission.id}",
            headers=auth_headers,
            json=asdict(permission),
        )
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        assert response.json["name"] == permission.name

    @pytest.mark.parametrize("user", [True], indirect=True)
    def test_delete(self, user, auth_headers, permission):
        """Тест на удаление права."""
        response = self.client.delete(
            f"{self.url}/{permission.id}", headers=auth_headers
        )
        self.assert_response(response, {"status_code": HTTPStatus.OK})
        response = self.client.get(f"{self.url}/{permission.id}", headers=auth_headers)
        self.assert_response(response, {"status_code": HTTPStatus.NOT_FOUND})
