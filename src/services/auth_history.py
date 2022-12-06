from src.services.base import BaseService
from src.models.auth_history import AuthEvent


class AuthHistoryService(BaseService):
    """Класс сервиса по работе с таблицей auth_history."""
    model = AuthEvent
