from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.core.config import postgres_settings

db = SQLAlchemy()


def init_db(app: Flask):
    """Инициализация базы данных."""
    from src.models import (auth_history, permissions,  # noqa: F401
                            relations, roles, user, social_account)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://{pg_user}:{pg_pass}@{pg_host}/{pg_dbname}".format(
        pg_user=postgres_settings.postgres_user,
        pg_pass=postgres_settings.postgres_password,
        pg_host=postgres_settings.db_host,
        pg_dbname=postgres_settings.postgres_db,
    )
    db.init_app(app)
