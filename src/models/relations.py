import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.db.db import db

user_role = db.Table(
    'user_role',
    db.Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    ),
    db.Column(
        'user', UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    ),
    db.Column(
        'role', UUID(as_uuid=True), db.ForeignKey("roles.id"), nullable=False
    )
)

role_permission = db.Table(
    'role_permission',
    db.Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    ),
    db.Column(
        'role', UUID(as_uuid=True), db.ForeignKey("roles.id"), nullable=False
    ),
    db.Column(
        'permission', UUID(as_uuid=True), db.ForeignKey("permissions.id"),
        nullable=False
    )
)
