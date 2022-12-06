import getpass

from flask import Flask

from src.services.user import UserService


def init_commands(app: Flask):
    """Инициализировать консольные команды Flask.

    Args:
        app: приложение Flask

    """
    @app.cli.command("createsuperuser")
    def createsuperuser():
        """Создать суперпользователя."""
        try:
            login = input('Введите логин: ')
            password1 = getpass.getpass('Введите пароль: ')
            password2 = getpass.getpass('Повторите пароль: ')
            if password1 != password2:
                raise Exception('Введенные пароли не совпадают')

            with app.app_context():
                UserService.create_superuser(login, password1)
                print(f'Суперпользователь {login} успешно создан.')

        except Exception:
            print('Ошибка создания суперпользователя')
            raise
