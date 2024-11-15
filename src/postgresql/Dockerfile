FROM python:3.10-slim

WORKDIR /app

# Workaround for quicker development.
# Installing required packages before copying the rest of the code avoids re-installing them on every code change.
# https://docs.docker.com/build/cache/

COPY ./postgresql/requirements.txt /app/postgresql/requirements.txt

RUN pip install --no-cache-dir -r postgresql/requirements.txt

COPY ./postgresql/ /app/postgresql/

WORKDIR /app/postgresql/
ENV PYTHONPATH=/app

ENTRYPOINT ["alembic"]
CMD ["upgrade", "head"]
