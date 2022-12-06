from flask import Blueprint, jsonify, request

from src.core.config import yandex_oauth2_settings
# TODO: uncomment from src.utils.decorators import superuser_required


ya = Blueprint("ya", __name__, url_prefix="/ya")


@ya.route("/client", methods=["GET"])
# TODO: uncomment @superuser_required()
def client():
    """Получить client_id Яндекс OAuth2."""

    return jsonify(client_id=yandex_oauth2_settings.client_id)


@ya.route('/verification_code', methods=["GET"])
def verification_code():
    """Callback для получения кода верификации."""

    code = request.args.get('code', None, type=int)
    return jsonify(code)