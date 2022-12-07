import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from src.db.db import db

LIST_KEYS_FILTEROUT_FROM_AS_DICT = ['_sa_instance_state']


def create_partition(target, connection, **kw) -> None:
    """Создать отдельные секции для различных user_device_type."""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_smart" PARTITION OF "auth_history" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_mobile" PARTITION OF "auth_history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_web" PARTITION OF "auth_history" FOR VALUES IN ('web')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_other" PARTITION OF "auth_history" FOR VALUES IN ('other');"""
    )


class AuthEvent(db.Model):
    """Модель для истории логинов."""

    __tablename__ = "auth_history"

    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        }
    )

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
    user_device_type = db.Column(db.Text, primary_key=True)

    def as_dict(self, except_keys: list[str] = LIST_KEYS_FILTEROUT_FROM_AS_DICT):
        """Return dict form of an object without except_keys"""
        return {k: v for k, v in self.__dict__.items() if k not in except_keys}
