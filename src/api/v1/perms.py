from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError

from src.api.v1 import response_messages
from src.models.permissions import Permission
from src.services.permission import PermissionService
from src.utils.decorators import superuser_required

parser = reqparse.RequestParser()
parser.add_argument(
    "name",
    type=str,
    help=response_messages.FIELD_CANNOT_BE_BLANK,
    required=True,
    trim=True,
)


resource_fields = {
    "id": fields.String,
    "name": fields.String,
}


class Permissions(Resource):

    service = PermissionService

    @superuser_required()
    @marshal_with(resource_fields)
    def get(self, obj_id=None):
        """Получить список прав."""
        if obj_id:
            perm = Permission.query.get(obj_id)
            return perm or (
                jsonify(response_messages.PERM_NOT_FOUND),
                HTTPStatus.NOT_FOUND,
            )
        return Permission.query.all()

    @superuser_required()
    @marshal_with(resource_fields)
    def post(self):
        """Создать право."""
        data = request.json
        if Permission.query.filter_by(name=data["name"]).first():
            return (
                jsonify(response_messages.PERM_ALREADY_EXIST),
                HTTPStatus.BAD_REQUEST,
            )
        return self.service.create(name=data["name"])

    @superuser_required()
    @marshal_with(resource_fields)
    def put(self, obj_id):
        """Изменить право."""
        data = request.json
        perm = Permission.query.get(obj_id)
        if not perm:
            return (
                jsonify(response_messages.PERM_NOT_FOUND),
                HTTPStatus.NOT_FOUND,
            )
        try:
            return self.service.update(perm, name=data["name"])
        except IntegrityError:
            return (
                jsonify(response_messages.PERM_ALREADY_EXIST),
                HTTPStatus.BAD_REQUEST,
            )

    @superuser_required()
    def delete(self, obj_id):
        """Удалить право."""
        perm = Permission.query.get(obj_id)
        if not perm:
            return (
                jsonify(response_messages.PERM_NOT_FOUND),
                HTTPStatus.NOT_FOUND,
            )
        self.service.delete(perm)
