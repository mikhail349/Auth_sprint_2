import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.db.db import db


class Permission(db.Model):
    """Модель для прав."""

    __tablename__ = "permissions"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(length=100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return str(self.id)
