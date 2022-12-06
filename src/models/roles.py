import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.db import db
from src.models.permissions import Permission
from src.models.relations import role_permission


class Role(db.Model):
    """Модель для роли."""

    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(length=100), unique=True, nullable=False)
    permissions = relationship(
        Permission,
        secondary=role_permission,
        backref="roles",
        cascade="all,delete",
    )
