# API-сервис аутентификации и управления правами

Основной репозиторий находится [тут](https://github.com/mikhail349/Auth_sprint_2)

В качестве ETL проекта используется [данный репозиторий](https://github.com/mikhail349ya/new_admin_panel_sprint_3)

## Документация API (Swagger)

1. API личного кабинета пользователя доступно по api `/api/v1/openapi/account`
2. API администратора прав и ролей доступно по api `/api/v1/openapi/admin`

## Первый запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
2. Создать docker volume для Postgres `docker volume create pg_auth`
3. Запустить докер `docker compose up --build`

## Первый локальный запуск

1. Сформировать виртуальное Python-окружение `python -m venv venv`
2. Установить зависимости `pip install -r requirements`
3. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
4. Запустить Postgres и Redis
5. Перейти в папку с приложением `cd src/app`
6. Применить миграции `flask db upgrade`
7. Запустить приложение `python wsgi.py`

## Миграция после внесения изменений в `src/models`

1. Перейти в папку с приложением `cd src/app`
2. Создать файл миграций `flask db migrate -m "<Краткое описание изменений в БД>"`
3. Применить миграции `flask db upgrade`

## Создание суперпользователя

1. Перейти в папку с приложением `cd src/app`
2. Выполнить команду `flask createsuperuser` и следовать инструкциям

## Линтер

Запуск: в корне проекта `flake8`. Для настройки используется файл `setup.cfg`

## Тестирование

1. Перейти в папку с тестами `cd tests/functional`
2. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
3. Создать docker volume для Postgres `docker volume create pg_auth_test`
4. Запустить докер `docker compose up --build`