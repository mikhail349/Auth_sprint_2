from src.db.db import db


class BaseService:
    """Базовый класс сервиса по CRUD операциям в БД."""
    model: db.Model = None

    @classmethod
    def create(self, **kwargs) -> model:
        """Создать объект в БД.

        Args:
            **kwargs: аргументы

        Returns
            model: объект

        """
        obj = self.model(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def update(self, obj, **kwargs) -> model:
        """Обновить объект в БД.

        Args:
            obj: инстанс объекта
            **kwargs: аргументы

        Returns
            model: объект

        """
        for k, v in kwargs.items():
            setattr(obj, k, v)
        db.session.commit()
        return obj

    @classmethod
    def delete(self, obj):
        """Удалить объект из БД.

        Args:
            obj: инстанс объекта

        """
        db.session.delete(obj)
        db.session.commit()
