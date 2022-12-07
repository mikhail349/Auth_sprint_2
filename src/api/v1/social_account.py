from http import HTTPStatus

from flask import Blueprint, Response, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models.user import User
from src.models.social_account import SocialAccount
from src.services.social_account import SocialAccountService
from src.api.v1 import response_messages


social_account = Blueprint("social_account", __name__,  url_prefix="social_account")


@social_account.route("/<string:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    """Удалить свою запись из реестра связанных аккаунтов соцсетей."""

    identity = get_jwt_identity()
    user = User.query.filter_by(login=identity).one_or_none()
    social_account = SocialAccount.query.filter_by(id=id, user_id=user.id).one_or_none()
    if not social_account:
        return jsonify(response_messages.SOCIAL_ACCOUNT_NOT_FOUND), HTTPStatus.NOT_FOUND

    SocialAccountService.delete(social_account)
    return Response(status=HTTPStatus.OK)
