from contextlib import contextmanager

from src.db.db import db


@contextmanager
def transaction():
    """Контекстный менеджер транзакции."""
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
