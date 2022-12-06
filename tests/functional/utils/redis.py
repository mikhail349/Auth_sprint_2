from redis import Redis
from redis.exceptions import ConnectionError
import backoff

from src.core.config import redis_settings


@backoff.on_exception(backoff.expo, exception=ConnectionError)
def flush_redis():
    """Очистить данные в Redis."""
    def db_flush(db: int):
        """Очистить данные в DB Redis.

        Args:
            db: номер БД

        """
        redis.select(db)
        redis.flushall()

    redis = Redis(host=redis_settings.redis_host,
                  port=redis_settings.redis_port)

    db_flush(redis_settings.redis_db_tokens_revoked)
    db_flush(redis_settings.redis_db_tokens_access_refresh_map)
