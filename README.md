
<h1 align="center">API для управления библиотекой</h1>

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-8B3E2F?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![pytest](https://img.shields.io/badge/pytest-3670A0?style=for-the-badge&logo=pytest&logoColor=ffdd54)](https://pytest.org/)
</div>

Выполнено в рамках [тестового задания](https://app.affine.pro/workspace/f6dfe706-59c0-41e5-898b-9d6a25d84efe/Yv_Z_9aEQMmAY1oZJ69hJ)

## Установка и запуск:

1. Склонируйте репозиторий и перейдите в папку

```
git clone https://github.com/pavlowave/fastapi_library_management
cd fastapi_library_management
```

2. Активируйте вирутальное окружение:

Для Linux (и macOS):
```bash
mkvirtualenv venv
workon venv
```
для Windows:
```bash
python -m venv venv
venv\Scripts\activate 
```

3. Устанавливаем зависимости :
```bash
pip install -r requirements.txt
```

4. Создаем файл .env со следующим содержимым:
```
DB_NAME=myname_db
DB_USER=myname_db
DB_PASSWORD=myname_db
DB_HOST=localhost
DB_PORT=5432
```
5. Создаем БД:

Откройте терминал и подключитесь к PostgreSQL под суперпользователем (например, postgres):
```bash
psql -U postgres
```
Если PostgreSQL защищён паролем, введите его при запросе.

Создайте базу данных с именем myname_db:
```bash
CREATE DATABASE myname_db;
```
Создайте пользователя с именем myname_db и задайте пароль:
```bash
CREATE USER myname_db WITH PASSWORD 'myname_db';
```
Предоставьте пользователю myname_db полный доступ к базе данных myname_db:
```bash
GRANT ALL PRIVILEGES ON DATABASE myname_db TO myname_db;
```
Cуперправа:
```bash
ALTER USER myname_db WITH SUPERUSER;
```
5. Запустите тесты:
```bash
pytest tests\test_api.py
```
6. Запустите сервер:
```bash
uvicorn app.main:app --reload
```
## Использование

Документация API доступна по адресу:

- http://127.0.0.1:8000/redoc/ (Redoc)
- http://127.0.0.1:8000/swagger/ (Swagger)

