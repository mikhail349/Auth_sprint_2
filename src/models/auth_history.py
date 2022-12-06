import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.db.db import db

LIST_KEYS_FILTEROUT_FROM_AS_DICT = ['_sa_instance_state']


class AuthEvent(db.Model):
    """Модель для истории логинов."""

    __tablename__ = "auth_history"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    user_agent = db.Column(db.Text, nullable=False)
    logged_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )

    def as_dict(self, except_keys: list[str] = LIST_KEYS_FILTEROUT_FROM_AS_DICT):
        """Return dict form of an object without except_keys"""
        return {k: v for k, v in self.__dict__.items() if k not in except_keys}
