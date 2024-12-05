FROM python:3.10-slim

WORKDIR /app

COPY ./db_api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt 

COPY ./db_api /app/
COPY ./helpers ./helpers
COPY ./postgresql ./postgresql

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]