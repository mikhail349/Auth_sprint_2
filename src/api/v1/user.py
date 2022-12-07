from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

import src.api.v1.response_messages as messages
from src.app.extensions import jwt
from src.core.config import app_settings
from src.db.db import db  # noqa F401
from src.models.auth_history import AuthEvent
from src.models.user import User
from src.services.user import UserService
from src.storages.token import get_token_manager
from src.utils.decorators import superuser_required

user = Blueprint("user", __name__,  url_prefix="user")


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Define token revokation check mechanism."""

    jti = jwt_payload["jti"]
    token_manager = get_token_manager()
    return token_manager.is_jti_revoked(jti)


@user.route("/login", methods=["POST"])
def login():
    """Login endpoint."""

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # check username and password
    user = UserService.authenticate(username, password)
    if user is None:
        msg = jsonify(messages.LOGIN_INCORRECT)
        return msg, HTTPStatus.UNAUTHORIZED

    access_token, refresh_token = UserService.login(user)

    # set tokens to cookies
    response = jsonify(access_token=access_token, refresh_token=refresh_token)
    return response, HTTPStatus.OK


@user.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout endpoint"""

    # get access jti and revoke both access and refresh
    jwt_dict = get_jwt()
    if not jwt:
        return jsonify(messages.NOT_AUTHORIZED), HTTPStatus.UNAUTHORIZED

    jti = jwt_dict.get("jti")
    token_manager = get_token_manager()
    token_manager.revoke_both_by_access_jti(jti)

    response = jsonify(messages.LOGOUT_OK)
    return response, HTTPStatus.OK


@user.route("/refresh_token", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Token refresh endpoint"""

    identity = get_jwt_identity()
    jwt_dict = get_jwt()
    refresh_jti = jwt_dict.get("jti")

    # check refresh is revoked
    token_manager = get_token_manager()
    revoked = token_manager.is_jti_revoked(refresh_jti)

    if revoked:
        return jsonify(messages.REFRESH_FAILED), HTTPStatus.UNAUTHORIZED

    token_manager.revoke_token_jti(refresh_jti)
    user = User.query.filter_by(login=identity).one_or_none()
    access_token, refresh_token = UserService.create_tokens(user)
    return jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK


@user.route("/register", methods=["POST"])
def register():
    """Register new user endpoint"""

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify(messages.WRONG_INPUT), HTTPStatus.BAD_REQUEST

    # check username and password
    user = User.query.filter_by(login=username).one_or_none()

    if user:
        return jsonify(messages.USER_EXISTS), HTTPStatus.BAD_REQUEST

    # create user in db
    UserService.create(username, password)

    return jsonify(messages.USER_CREATED), HTTPStatus.OK


@user.route("/update", methods=["PUT"])
@jwt_required()
def update():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify(messages.WRONG_INPUT), HTTPStatus.BAD_REQUEST

    identity = get_jwt_identity()
    # check username and password
    user = User.query.filter_by(login=identity).one_or_none()

    if not user:
        return jsonify(messages.USER_DOESNT_EXIST), HTTPStatus.BAD_REQUEST

    # update user in db
    UserService.update(user, login=username, password=password)

    access_token, refresh_token = UserService.create_tokens(user)
    return jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK


@user.route("/login_history", methods=["GET"])
@jwt_required()
def login_history():
    """Get user login history endpoint"""

    # collect history
    identity = get_jwt_identity()
    user = User.query.filter_by(login=identity).one_or_none()
    if not user:
        return jsonify(messages.USER_DOESNT_EXIST), HTTPStatus.BAD_REQUEST
    page = request.args.get('page', app_settings.default_page, type=int)
    size = request.args.get('size', app_settings.default_page_size, type=int)
    history = AuthEvent.query.filter_by(user=user.id).paginate(page=page,
                                                               per_page=size)
    return jsonify([entry.as_dict() for entry in history]), HTTPStatus.OK


@user.route("/<string:user_id>/roles/<string:role_name>", methods=["POST"])
@superuser_required()
def set_role(user_id, role_name):
    """Добавить пользователю роль."""
    user = User.query.get(user_id)
    if not user:
        return jsonify(messages.USER_DOESNT_EXIST), HTTPStatus.BAD_REQUEST
    UserService.set_role(user, role_name)
    return jsonify(messages.USER_ROLES_UPDATED), HTTPStatus.OK


@user.route("/<string:user_id>/roles/<string:role_name>", methods=["DELETE"])
@superuser_required()
def remove_role(user_id, role_name):
    """Удалить роль у пользователя."""
    user = User.query.get(user_id)
    if not user:
        return jsonify(messages.USER_DOESNT_EXIST), HTTPStatus.BAD_REQUEST
    UserService.remove_role(user, role_name)
    return jsonify(messages.USER_ROLES_DELETED), HTTPStatus.OK
