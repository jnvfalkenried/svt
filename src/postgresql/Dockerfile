FROM python:3.10-slim

WORKDIR /app

COPY ./postgresql/ /app/postgresql/

RUN pip install --no-cache-dir -r postgresql/requirements.txt

WORKDIR /app/postgresql/
ENV PYTHONPATH=/app

ENTRYPOINT ["alembic"]
CMD ["upgrade", "head"]
