from src.db.db import db
from src.models.permissions import Permission
from src.models.roles import Role
from src.services.base import BaseService


class RoleService(BaseService):
    """Класс сервиса по CRUD операциям с таблицей roles."""

    model = Role

    @classmethod
    def create(self, name: str, perms: list):
        """Создать роль."""
        role = Role(name=name)
        db.session.add(role)
        for perm_id in perms:
            perm = Permission.query.get(perm_id)
            role.permissions.append(perm)
            db.session.add(role)
        db.session.commit()
        return role

    @classmethod
    def update(self, obj: Role, name: str, perms: list):
        """Изменить роль."""
        obj.name = name
        permissions = [Permission.query.get(perm_id) for perm_id in perms]
        obj.permissions = permissions
        db.session.add(obj)
        db.session.commit()
        return obj
