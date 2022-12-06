from http import HTTPStatus

from flask import Blueprint, request, jsonify

from src.services.user import UserService
from src.services.oauth2 import OAuth2


def create_blueprint(social_name: str, url_prefix: str,
                     client_id: str, client_secret: str,
                     token_url: str, base_url: str) -> Blueprint:
    """Создать blueprint, реализующий endoint /login?code=<code> для OAuth2.

    Args:
        social_name: имя социальной сети
        url_prefix: url префикс
        client_id: ИД клиента сервиса провайдера
        client_secret: секретный ключ клиента сервиса провайдера
        token_url: url для получения токена по коду
        base_url: базовый url API провайдера

    Returns:
        Blueprint: blueprint

    """
    blueprint = Blueprint(social_name, __name__, url_prefix=url_prefix)

    @blueprint.route("/login", methods=["GET"])
    def login():
        """Callback для логина по средством кода."""

        code = request.args.get("code", None, type=str)

        oauth2 = OAuth2(client_id=client_id, client_secret=client_secret, token_url=token_url, base_url=base_url)

        response = oauth2.get_auth(code)
        auth = response.json()
        if response.status_code != HTTPStatus.OK:
            return jsonify(auth)

        response = oauth2.get_info(auth['access_token'])
        info = response.json()
        if response.status_code != HTTPStatus.OK:
            return jsonify(info)

        user = UserService.get_by_social_account(social_id=info['id'], social_name=social_name)
        if user:
            access_token, refresh_token = UserService.login(user)
            return jsonify(access_token=access_token, refresh_token=refresh_token)

        user = UserService.create_by_social_account(social_id=info['id'], social_name=social_name)
        access_token, refresh_token = UserService.login(user)

        return jsonify(access_token=access_token, refresh_token=refresh_token)

    return blueprint
