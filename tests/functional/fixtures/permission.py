import pytest

from src.services.permission import PermissionService
from tests.functional.src.lib.factory import generate_random_permission
from tests.functional.src.lib.models.permission import Permission


@pytest.fixture
def permission_data():
    """Сгенерированное случайное право."""
    return generate_random_permission()


@pytest.fixture
def permission(client, auth_headers, permission_data):
    """Право, созданное в приложении."""
    perm = PermissionService.create(name=permission_data.name)
    yield Permission(id=str(perm.id), name=perm.name)
    perm = PermissionService.model.query.get(perm.id)
    if perm:
        PermissionService.delete(perm)
