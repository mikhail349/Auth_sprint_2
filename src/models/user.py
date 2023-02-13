import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.db import db
from src.models.relations import user_role
from src.models.roles import Role
from src.models.auth_history import AuthEvent


class User(db.Model):
    """Модель для пользователя."""

    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String(length=100), unique=True, nullable=False)
    password = db.Column(db.String(length=100), nullable=False)
    email = db.Column(db.String(length=100), unique=True, nullable=False)
    roles = relationship(
        Role,
        secondary=user_role,
        backref="users",
        cascade="all,delete",
    )
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    auth_events = relationship(
        AuthEvent,
        cascade="all,delete"
    )

    def __repr__(self):
        return f"<User {self.login}>"
