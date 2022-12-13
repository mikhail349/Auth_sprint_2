from http import HTTPStatus
from typing import Callable

from flask import Blueprint, jsonify, request
import requests

from src.services.user import UserService


def create_blueprint(
    social_name: str,
    url_prefix: str,
    client_id: str,
    client_secret: str,
    auth_url: str,
    token_url: str,
    base_url: str,
    redirect_url: str,
    get_user_id: Callable,
    construct_auth_request: Callable = None,
    construct_info_request: Callable = None
) -> Blueprint:
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
        get_user_id: метод для получения идентификатора пользователя
        constuct_auth_request: метод для переопределения параметров запроса авторизации
        constuct_info_request: метод для переопределения параметров запроса информации

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

        response = get_auth(code)
        if response.status_code != HTTPStatus.OK:
            return (response.content, response.status_code, response.headers.items())
        auth = response.json()

        response = get_user_info(auth['access_token'])
        if response.status_code != HTTPStatus.OK:
            return (response.content, response.status_code, response.headers.items())
        info = response.json()

        user = UserService.get_or_create_by_social_account(
            social_id=get_user_id(info),
            social_name=social_name
        )
        access_token, refresh_token = UserService.login(user)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    def get_auth(code: str):
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
            "client_id": client_id,
            "client_secret": client_secret
        }
        if construct_auth_request:
            construct_auth_request(headers, data)
        return requests.post(token_url, headers=headers, data=data)

    def get_user_info(token: str):
        """Получить информацию о пользователе.

        Args:
            token: токен доступа

        Returns:
            Response: http ответ

        """
        headers = {}
        params = {}
        if construct_info_request:
            construct_info_request(token, headers, params)
        return requests.get(base_url, headers=headers, params=params)

    return blueprint
