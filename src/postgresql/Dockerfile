# Используем легковесный Python-образ
FROM python:3.10-slim

WORKDIR /app

COPY ./postgresql/alembic /app/alembic
COPY ./postgresql/database_models /app/database_models

COPY ./postgresql/alembic.ini /app
COPY ./postgresql/db.py /app/
COPY ./postgresql/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем команду запуска alembic upgrade head
ENTRYPOINT ["alembic"]
CMD ["upgrade", "head"]
