import requests
from datetime import datetime
from src.core.config import notifications_settings


class NotificationService:
    """Класс для работы с сервисом нотификаций."""

    def __init__(self, url):
        self.url = url
        self.user_registered_url = self.url + "/events/user_registered"

    def send_registration_link(self, username: str) -> requests.Response:
        """Отправить пользовалелю запрос на подтверждение регистрации
        через сервис нотификаций."""

        data = {
            "delivery_type": "email",
            "priority": "high",
            "body": {"username": username, "created_at": str(datetime.now())},
        }
        headers = {"Content-type": "application/json"}
        res = requests.post(
            self.user_registered_url, json=data, headers=headers
        )
        return res


notification_service = NotificationService(
    notifications_settings.notifications_api)
