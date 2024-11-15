FROM python:3.10-slim

WORKDIR /app

COPY ./db_api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./db_api /app
COPY ./postgresql/config /app/postgresql/config
COPY ./postgresql/database_models /app/postgresql/database_models
COPY ./postgresql/database_scripts /app/postgresql/database_scripts

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]