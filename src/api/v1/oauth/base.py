from http import HTTPStatus
from typing import Callable

from flask import Blueprint, jsonify, request

from src.services.oauth2 import OAuth2
from src.services.user import UserService


def create_blueprint(social_name: str, url_prefix: str,
                     client_id: str, client_secret: str,
                     auth_url: str, token_url: str, base_url: str,
                     redirect_url: str, get_id: Callable) -> Blueprint:
    """Создать blueprint, реализующий endpoint /login для OAuth2.

    Args:
        social_name: имя социальной сети
        url_prefix: url префикс
        client_id: ИД клиента сервиса провайдера
        client_secret: секретный ключ клиента сервиса провайдера
        auth_url: url для получения кода
        token_url: url для получения токена по коду
        base_url: базовый url API провайдера
        redirect_url: url для callback, куда будет передан код авторизации
        get_id: метод для получения идентификатора пользователя

    Returns:
        Blueprint: blueprint

    """
    blueprint = Blueprint(social_name, __name__, url_prefix=url_prefix)

    @blueprint.route("/info", methods=["GET"])
    def get_info():
        """Получить данные, необходимые для OAuth2."""
        return jsonify(client_id=client_id, auth_url=auth_url, redirect_url=redirect_url)

    @blueprint.route("/tokens", methods=["GET"])
    def get_tokens():
        """Получить токены доступа посредством OAuth2 кода."""
        code = request.args.get("code")
        oauth2 = OAuth2(
            client_id=client_id, client_secret=client_secret, token_url=token_url,
            base_url=base_url, redirect_url=redirect_url)
        response = oauth2.get_auth(code)
        auth = response.json()
        if response.status_code != HTTPStatus.OK:
            return (response.content, response.status_code, response.headers.items())

        response = oauth2.get_info(auth['access_token'])
        info = response.json()
        if response.status_code != HTTPStatus.OK:
            return (response.content, response.status_code, response.headers.items())

        user = UserService.get_or_create_by_social_account(
            social_id=get_id(info), social_name=social_name)
        access_token, refresh_token = UserService.login(user)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    return blueprint
