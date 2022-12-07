import requests
from requests import Response


class OAuth2:
    """Класс работы с OAuth2.

    Args:
        client_id: ИД клиента сервиса провайдера
        client_secret: секретный ключ клиента сервиса провайдера
        token_url: url для получения токена по коду
        base_url: базовый url API провайдера

    """
    def __init__(self, client_id: str, client_secret: str, token_url: str, base_url: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.base_url = base_url

    def get_auth(self, code: str) -> Response:
        """Получить авторизационные данные.

        Args:
            code: код авторизации

        Returns:
            Response: http ответ

        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        return requests.post(self.token_url, headers=headers, data=data)

    def get_info(self, token: str) -> Response:
        """Получить информацию о пользователе.

        Args:
            token: токен доступа

        Returns:
            Response: http ответ

        """
        headers = {
            "Authorization": "bearer {}".format(token)
        }

        params = {
            "format": "json"
        }
        return requests.get(self.base_url, headers=headers, params=params)
