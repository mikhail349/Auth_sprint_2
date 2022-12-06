from src.services.base import BaseService
from src.models.social_account import SocialAccount


class SocialAccountService(BaseService):
    """Класс сервиса по работе с таблицей social_accounts."""
    model = SocialAccount
