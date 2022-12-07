import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.db.db import db
from src.models.user import User


class SocialAccount(db.Model):
    """Модель привязанных аккаунтов пользователя."""

    __tablename__ = "social_accounts"
    __table_args__ = (db.UniqueConstraint('social_id', 'social_name',
                                          name='social_unique'),)

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=False
    )
    user = db.relationship(
        User,
        backref=db.backref('social_accounts', lazy=True)
    )

    social_id = db.Column(db.String(length=255), nullable=False)
    social_name = db.Column(db.String(length=255), nullable=False)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
