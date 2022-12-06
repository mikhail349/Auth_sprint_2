from src.models.permissions import Permission
from src.services.base import BaseService


class PermissionService(BaseService):
    """Класс сервиса по CRUD операциям с таблицей permissions."""

    model = Permission
