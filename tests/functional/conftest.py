import pytest

from src.app.app import app as current_app
from tests.functional.src.base import TestBase
from tests.functional.utils.redis import flush_redis

pytest_plugins = (
    "tests.functional.fixtures.user",
    "tests.functional.fixtures.permission",
    "tests.functional.fixtures.role",
)


@pytest.fixture(scope="session")
def app():
    """Фикстура приложения Flask."""
    with current_app.app_context():
        flush_redis()
        yield current_app
        flush_redis()


@pytest.fixture(scope="class")
def client(app, request):
    """Фикстура клиента Flask."""
    client = app.test_client()
    request.cls.client = client
    yield client


@pytest.fixture
def auth_headers(auth):
    """Фикстура заголовков с авторизацией."""
    return TestBase().get_auth_header(auth['access_token'])
