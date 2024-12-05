FROM python:3.10-slim

WORKDIR /app

COPY ./webapp/backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt 

COPY ./webapp/backend /app/
COPY ./src/helpers ./helpers
COPY ./src/postgresql ./postgresql

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
