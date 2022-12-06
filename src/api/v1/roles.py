from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError

from src.api.v1 import response_messages
from src.models.roles import Role
from src.services.roles import RoleService
from src.utils.decorators import superuser_required

parser = reqparse.RequestParser()
parser.add_argument(
    "name",
    type=str,
    help=response_messages.FIELD_CANNOT_BE_BLANK,
    required=True,
    trim=True,
)
parser.add_argument(
    "params",
    type=list,
    help=response_messages.FIELD_CANNOT_BE_BLANK,
    required=True,
    trim=True,
)


resource_fields = {
    "id": fields.String,
    "name": fields.String,
    "perms": fields.List(
        fields.String, attribute=lambda x: getattr(x, "permissions", None)),
}


class Roles(Resource):

    service = RoleService

    @superuser_required()
    @marshal_with(resource_fields)
    def get(self, obj_id=None):
        """Получить список ролей."""
        if obj_id:
            role = Role.query.get(obj_id)
            return role or (
                jsonify(response_messages.PERM_NOT_FOUND),
                HTTPStatus.NOT_FOUND,
            )
        return Role.query.all()

    @superuser_required()
    @marshal_with(resource_fields)
    def post(self):
        """Создать роль."""
        name = request.json["name"]
        perms = request.json["perms"]
        if Role.query.filter_by(name=name).first():
            return (
                jsonify(response_messages.ROLE_ALREADY_EXIST),
                HTTPStatus.BAD_REQUEST,
            )
        return self.service.create(name=name, perms=perms)

    @superuser_required()
    @marshal_with(resource_fields)
    def put(self, obj_id):
        """Изменить роль."""
        name = request.json["name"]
        perms = request.json["perms"]
        role = Role.query.get(obj_id)
        if not role:
            return (
                jsonify(response_messages.ROLE_NOT_FOUND),
                HTTPStatus.NOT_FOUND,
            )
        try:
            return self.service.update(role, name, perms)
        except IntegrityError:
            return (
                jsonify(response_messages.PERM_ALREADY_EXIST),
                HTTPStatus.BAD_REQUEST,
            )

    @superuser_required()
    def delete(self, obj_id):
        """Удалить роль."""
        role = Role.query.get(obj_id)
        if not role:
            return (
                jsonify(response_messages.ROLE_NOT_FOUND),
                HTTPStatus.NOT_FOUND,
            )
        self.service.delete(role)
