FROM python:3.10-slim

WORKDIR /app

COPY ./postgresql/ /app/src/postgresql/

RUN pip install --no-cache-dir -r src/postgresql/requirements.txt

WORKDIR /app/src/postgresql/

ENTRYPOINT ["alembic"]
CMD ["upgrade", "head"]
