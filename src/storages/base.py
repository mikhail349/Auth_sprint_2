from abc import abstractmethod, ABC
from typing import Optional, Any


class CacheStorage(ABC):
    """Абстрактный класс хранилища кэша."""

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Существует ли ключ в хранилище.

        Args:
            key: ключ

        Returns:
            bool: Да/нет
        """
        pass

    @abstractmethod
    def put(self, key: str, value: Optional[Any] = None,
            timeout: Optional[int] = None):
        """Записать данные в хранилище.

        Args:
            key: ключ
            value: значение
            timeout: таймаут в секундах
        """
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Получить данные по ключу.

        Args:
            key: ключ

        Returns:
            Optional[Any]: данные
        """
        pass
