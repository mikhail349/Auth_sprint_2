import pytest

from src.services.roles import RoleService
from tests.functional.src.lib.factory import generate_random_role
from tests.functional.src.lib.models.role import Role


@pytest.fixture
def role_data(permission):
    """Сгенерированная случайная роль."""
    return generate_random_role(perms=[permission.id])


@pytest.fixture
def role(client, auth_headers, role_data):
    """Роль, созданная в приложении."""
    role = RoleService.create(name=role_data.name, perms=role_data.perms)
    yield Role(id=str(role.id), name=role.name,
               perms=[str(perm) for perm in role.permissions])
    role = RoleService.model.query.get(role.id)
    if role:
        RoleService.delete(role)
