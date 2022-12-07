from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask import request

from src.db.db import db
from src.models.roles import Role
from src.models.user import User
from src.models.social_account import SocialAccount
from src.services.base import BaseService
from src.services.auth_history import AuthHistoryService
from src.storages.token import get_token_manager
from src.utils.context_managers import transaction
from src.utils.random import generate_string


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
    def create_by_social_account(cls, social_id: str, social_name: str) -> User:
        """Создать пользователя по аккаунту из соц. сети.

        Args:
            social_id: ИД пользователя в соц. сети
            social_name: название соц. сети

        Returns:
            User: пользователь

        """
        with transaction():
            login = cls.generate_login()
            password = generate_string()

            user = cls.model(login=login, password=cls.hash_password(password))
            social_account = SocialAccount(user=user, social_id=social_id, social_name=social_name)
            db.session.add(user)
            db.session.add(social_account)

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
    def generate_login(cls) -> str:
        """Сгенерировать логин.

        Returns:
            str: логин

        """
        login = generate_string()
        while cls.model.query.filter_by(login=login).first():
            login = generate_string()
        return login

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
    def login(cls, user: User) -> tuple[str, str]:
        """Залогинить пользователя.

        Args:
            user: пользователь

        Returns:
            tuple[str, str]: access-token, refresh-token

        """
        access_token, refresh_token = cls.create_tokens(user)

        token_manager = get_token_manager()
        token_manager.set_access_refresh_map(access_token, refresh_token)

        user_agent = request.headers.get("User-Agent")
        AuthHistoryService.create(
            user=user.id,
            user_agent=user_agent,
            user_device_type=cls.get_user_device_type(user_agent)
        )
        return access_token, refresh_token

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
    def get_by_social_account(cls, social_id: str, social_name: str) -> User | None:
        """Получить пользователя по аккаунту из соц. сети.

        Args:
            social_id: ИД пользователя в соц. сети
            social_name: название соц. сети

        Returns:
            User | None: пользователь или None

        """
        account = (
            SocialAccount.query
                         .filter_by(social_id=social_id, social_name=social_name)
                         .one_or_none()
        )
        if account:
            return account.user

    @classmethod
    def get_or_create_by_social_account(cls, social_id: str, social_name: str) -> User:
        """Получить или создать, если не существует, пользователя по аккаунту из соц. сети.

        Args:
            social_id: ИД пользователя в соц. сети
            social_name: название соц. сети

        Returns:
            User: пользователь

        """
        user = cls.get_by_social_account(social_id=social_id, social_name=social_name)
        if not user:
            user = cls.create_by_social_account(social_id=social_id, social_name=social_name)
        return user

    @classmethod
    def set_role(self, user: User, role_name: str) -> User:
        """Назначить роль пользователю."""
        role = Role.query.filter_by(name=role_name).first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def remove_role(cls, user: User, role_name: str):
        """Удалить роль у пользователя."""
        role = Role.query.filter_by(name=role_name).first()
        user.roles.remove(role)
        db.session.add(user)
        db.session.commit()
    
    @classmethod
    def remove_social_account(cls, user: User, social_account: SocialAccount):
        """Отвязать аккаунт соцсети."""
        user.social_accounts.remove(social_account)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user_device_type(user_agent: str) -> str:
        """Возвращает значение user_device_type на основе user agent."""
        for device in ["smart", "mobile", "web"]:
            if device in user_agent.lower():
                return device
        return "other"
