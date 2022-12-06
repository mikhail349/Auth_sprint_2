from typing import Optional, Any

from redis import Redis
from redis.exceptions import ConnectionError
import backoff

from src.storages.base import CacheStorage


class RedisStorage(CacheStorage):
    """Класс хранилища Redis.

    Args:
        redis: соединение с Redis

    """
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def exists(self, token: str) -> bool:
        return bool(self.redis.exists(token))

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def put(self, key: str, value: Optional[Any] = '',
            timeout: Optional[int] = None):
        self.redis.set(key, value, ex=timeout)

    @backoff.on_exception(backoff.expo, exception=ConnectionError)
    def get(self, key: str) -> Optional[Any]:
        return self.redis.get(key)
