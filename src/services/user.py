from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_jwt_extended import (create_access_token, create_refresh_token)

from src.db.db import db
from src.models.roles import Role
from src.models.user import User
from src.services.base import BaseService


class UserService(BaseService):
    """Класс сервиса по работе с таблицей users."""
    model = User

    @classmethod
    def create(cls, login: str, password: str, **kwargs) -> User:
        """Создать пользователя.

        Args:
            login: логин
            password: пароль
            **kwargs: остальные агрументы

        Returns:
            User: пользователь

        """
        user = cls.model(login=login,
                         password=cls.hash_password(password),
                         **kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def update(cls, user: User, login: str, password: str, **kwargs) -> User:
        """Обновить пользователя.

        Args:
            user: инстанс пользователя
            login: логин
            password: пароль
            **kwargs: остальные агрументы

        Returns:
            User: пользователь

        """
        user.login = login
        user.password = cls.hash_password(password)
        for k, v in kwargs.items():
            setattr(user, k, v)
        db.session.commit()
        return user

    @classmethod
    def create_superuser(cls, login: str, password: str) -> User:
        """Создать суперпользователя.

        Args:
            login: логин
            password: пароль

        Returns:
            User: пользователь

        """
        return cls.create(login=login, password=password, is_superuser=True)

    @classmethod
    def authenticate(cls, login: str, password: str) -> User | None:
        """Аутентифицировать пользователя.

        Args:
            login: логин
            password: пароль

        Returns:
            User | None: Пользователь или None

        """
        user = User.query.filter_by(login=login).one_or_none()
        if not user:
            return None

        try:
            ph = PasswordHasher()
            ph.verify(user.password, password)
            return user
        except VerifyMismatchError:
            return None

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Захэшировать пароль.

        Args:
            password: пароль

        Returns:
            str: хэшированный пароль

        """
        ph = PasswordHasher()
        return ph.hash(password)

    @classmethod
    def get_permissions(cls, login: str) -> list:
        """Получить права пользователя по логину.

        Args:
            login: логин

        Returns:
            list: список прав

        """
        user = (
            User.query
                .options(db.joinedload(User.roles)
                           .joinedload(Role.permissions))
                .filter_by(login=login)
                .first()
        )
        if not user:
            return []

        permissions = set()
        for role in user.roles:
            permissions = permissions.union(
                {perm.name for perm in role.permissions}
            )
        return list(permissions)

    @classmethod
    def create_tokens(cls, user: User) -> tuple[str, str]:
        """Создать токены для пользователя.

        Args:
            user: пользователь

        Returns:
            tuple[str, str]: access-token и refresh-token

        """
        additional_claims = {
            "permissions": UserService.get_permissions(user.login),
            "is_superuser": user.is_superuser,
        }
        access_token = create_access_token(identity=user.login, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=user.login)
        return access_token, refresh_token

    @classmethod
    def set_role(self, user: User, role_name: str) -> User:
        """Назначить роль пользователю."""
        role = Role.query.filter_by(name=role_name).first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def remove_role(self, user: User, role_name: str):
        """Удалить роль у пользователя."""
        role = Role.query.filter_by(name=role_name).first()
        user.roles.remove(role)
        db.session.add(user)
        db.session.commit()
