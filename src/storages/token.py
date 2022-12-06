from flask_jwt_extended import get_jti
from redis import Redis
from flask import current_app

from src.core.config import jwt_settings
from src.storages.redis_storage import RedisStorage
from src.storages.base import CacheStorage

TIMEOUT_STORAGE_ACCESS_TOKEN = 3600
TIMEOUT_STORAGE_REFRESH_TOKEN = 86400


class TokenManager:
    def __init__(
        self,
        storage_revoked: CacheStorage,
        storage_access_refresh_map: CacheStorage,
        timeout_access: int = TIMEOUT_STORAGE_ACCESS_TOKEN,
        timeout_refresh: int = TIMEOUT_STORAGE_REFRESH_TOKEN,
    ) -> None:

        # set timeouts
        self.timeout_access = timeout_access
        self.timeout_refresh = timeout_refresh

        # set token storages
        self.storage_revoked = storage_revoked
        self.storage_access_refresh_map = storage_access_refresh_map

    def set_access_refresh_map(self, access_token: str, refresh_token: str) -> None:
        """ Set access/refresh mapping with timeout.
            The mapping stores jtis."""
        access_jti = get_jti(access_token)
        refresh_jti = get_jti(refresh_token)
        self.storage_access_refresh_map.put(key=access_jti, value=refresh_jti, timeout=self.timeout_access)

    def revoke_token_jti(self, token_jti: str, timeout: int = None) -> None:
        """ Add a token to revocation storage. """
        timeout = timeout if timeout else self.timeout_refresh
        self.storage_revoked.put(key=token_jti, value=1, timeout=timeout)

    def revoke_token(self, token: str, timeout: int = None) -> None:
        """ Add a token to revocation storage. """
        token_jti = get_jti(token)
        self.revoke_token_jti(token_jti=token_jti, timeout=timeout)

    def revoke_both_by_access_jti(self, access_jti: str) -> int:
        """ Get refresh token from access/refresh mapping and add both tokens to revovation list. """
        refresh_jti = self.storage_access_refresh_map.get(access_jti)
        if refresh_jti:
            self.revoke_token_jti(refresh_jti, self.timeout_refresh)
        self.revoke_token_jti(access_jti, self.timeout_access)

    def is_jti_revoked(self, token_jti: str) -> bool:
        """ Check if token jti is in revocation list. """
        return self.storage_revoked.exists(token_jti)

    def is_token_revoked(self, token: str) -> bool:
        """ Check if token is revoked. """
        token_jti = get_jti(token)
        return self.is_jti_revoked(token_jti)


# specific managers
def get_redis_token_manager():
    """ Return an instance of redis token manager. """

    redis_revoked = Redis(
        host=current_app.config['REDIS_HOST'],
        port=current_app.config['REDIS_PORT'],
        db=current_app.config['REDIS_DB_TOKENS_REVOKED']
    )
    redis_access_refresh_map = Redis(
        host=current_app.config['REDIS_HOST'],
        port=current_app.config['REDIS_PORT'],
        db=current_app.config['REDIS_DB_TOKENS_ACCESS_REFRESH_MAP']
    )

    return TokenManager(
        RedisStorage(redis_revoked),
        RedisStorage(redis_access_refresh_map),
        jwt_settings.jwt_access_token_expires,
        jwt_settings.jwt_refresh_token_expires
    )


def get_token_manager():
    return get_redis_token_manager()
