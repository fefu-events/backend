![Logo](.github/assets/logo.png)

-----

Серверная часть [FEFU Events](https://github.com/fefu-events/fefu-events).

# Быстрый старт

Склонируйте проект
```bash
git clone https://github.com/fefu-events/fefu-events-backend.git
cd fefu-events-backend
```
Создайте файл ``.env`` в корне проекта и установите переменные
среды:
```bash
touch .env
echo DATABASE_URL=DATABASE_URL > .env
echo APP_CLIENT_ID=APP_CLIENT_ID > .env
echo TENANT_ID=TENANT_ID > .env
echo OPENAPI_CLIENT_ID=OPENAPI_CLIENT_ID > .env
echo SECRET_KEY=$(openssl rand -hex 32) > .env
```
Для запуска необходимо выполнить команды:
```bash
docker-compose build
docker-compose up -d
```

# Подготовка среды для разработки
Выполните следующие команды, чтобы загрузить вашу среду с ``poetry``: 
```bash
poetry install
poetry shell
```

# Запуск тестов
TODO

# Документация
Документация доступна по ручкам ``/docs`` или ``/redoc`` с помощью
Swagger или ReDoc соотвественно.

# Структура проекта

```
alembic         - миграции
app
├───routers     - ручки
├───models      - SQL модели и Pydantic схемы
├───config.py   - управление переменными среды
└───database.py - engine, session
```
