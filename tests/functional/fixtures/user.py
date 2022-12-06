import pytest

from src.services.user import UserService
from tests.functional.src.test_user import TestUser
from tests.functional.const import auth as auth_const
from tests.functional.const.api import user as api


@pytest.fixture(params=[False])
def user(request):
    """Фикстура пользователя.
    Для создания суперпользователя передать True в параметрах."""
    user = UserService.create(auth_const.LOGIN, auth_const.PASSWORD,
                              is_superuser=request.param)
    yield user
    UserService.delete(user)


@pytest.fixture
def auth(user, client):
    """Фикстура аутентификации."""

    body = {
        "username": auth_const.LOGIN,
        "password": auth_const.PASSWORD
    }
    user_url = TestUser().url
    response = client.post(f'{user_url}{api.LOGIN}', json=body)

    yield {
        'user': user,
        'access_token': response.json['access_token'],
        'refresh_token': response.json['refresh_token']
    }
