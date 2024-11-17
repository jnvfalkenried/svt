FROM python:3.10

WORKDIR /app

COPY ./db_api/requirements.txt .
# Add required packages including scipy
RUN pip install --no-cache-dir -r requirements.txt \
    google-cloud-aiplatform \
    vertexai \
    scipy \
    numpy

COPY ./db_api .
COPY ./helpers ./helpers
COPY ./postgresql ./postgresql

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]