import datetime

from redis import Redis

from src.core.config import app_settings, redis_settings


redis_conn = Redis(
    host=redis_settings.redis_host,
    port=redis_settings.redis_port,
    db=redis_settings.redis_db_tokens_rate_limit,
)


def is_request_limit_exceeded(identifier: str) -> bool:
    """Проверить, превышает ли число запросов от пользователя в минуту
    установленный лимит."""
    pipe = redis_conn.pipeline()
    now = datetime.datetime.now()
    key = f"{identifier}:{now.minute}"
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = pipe.execute()
    request_number = result[0]
    if request_number > app_settings.rate_limit:
        return True
    return False
