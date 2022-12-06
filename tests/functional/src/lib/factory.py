import random
import string
import uuid

from tests.functional.src.lib.models.permission import Permission
from tests.functional.src.lib.models.role import Role


def get_random_string(length=10):
    """Возвращает случайную строку."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_random_permission(id: str = None, name: str = None) -> Permission:
    """Возвращает рандомный объект Permission.
    Args:
        id: идентификатор (по умолчанию - сгенерировать)
        name: название (по умолчанию - сгенерировать)
    """
    return Permission(
        id=id or str(uuid.uuid4()), name=name or get_random_string()
    )


def generate_random_role(id: str = None, name: str = None, perms: list = None) -> Role:
    """Возвращает рандомный объект Role.
    Args:
        id: идентификатор (по умолчанию - сгенерировать)
        name: название (по умолчанию - сгенерировать)
        perms: list of permissions (по умолчанию - сгенерировать)
    """
    return Role(
        id=id or str(uuid.uuid4()), name=name or get_random_string(),
        perms=perms or [generate_random_permission()]
    )
