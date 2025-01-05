Usage
=====

..
    _How to start the scraper, backend, and frontend.
    _Configuration options (e.g., RabbitMQ URLs, environment variables).

Once the containers are up and running, you can access and configure the services as follows:

Accessing Services
------------------

1. **FastAPI**:
   - Access the FastAPI documentation at: `http://localhost/docs`

2. **RabbitMQ**:
   - Access the RabbitMQ web interface at: `http://localhost:15672`

3. **PostgreSQL**:
   - Access the PostgreSQL database by running the following command:

     .. code-block:: bash

        docker exec -it svt-postgres-1 psql -U postgres -d svt_db

Configuration Options
---------------------

Environment Variables

General Environment

- `ENVIRONMENT`: Specifies the deployment environment. Options: `[dev, stage, prod]`

RabbitMQ Configuration

- `RABBITMQ_USER`: RabbitMQ username.
- `RABBITMQ_PASS`: RabbitMQ password.
- `RABBITMQ_HOST`: RabbitMQ host (default: `rabbitmq`).
- `RABBITMQ_PORT`: RabbitMQ port.
- `RABBITMQ_UI_PORT_MAP`: Port mapping for the RabbitMQ web interface.

RabbitMQ Naming Configuration

- `RABBITMQ_EXCHANGE`: Default RabbitMQ exchange.
- `RMQ_TASKS_EXCHANGE`: Exchange for task-related messages.
- `RABBITMQ_HASHTAG_QUEUE`: Queue for hashtag-related messages.
- `RABBITMQ_VIDEO_BYTES_QUEUE`: Queue for video bytes.
- `RABBITMQ_EMBEDDINGS_QUEUE`: Queue for embeddings.
- `RMQ_PRODUCER_TASKS_QUEUE`: Producer task queue.

PostgreSQL Configuration

- `POSTGRES_USER`: PostgreSQL username.
- `POSTGRES_PASSWORD`: PostgreSQL password.
- `POSTGRES_DB`: PostgreSQL database name.
- `POSTGRES_HOST`: PostgreSQL host (default: `postgres`).
- `POSTGRES_PORT`: PostgreSQL port.
- `POSTGRES_PORT_MAP`: Port mapping for PostgreSQL.

Google Cloud Configuration

- `GOOGLE_PROJECT_ID`: Google Cloud project ID.
- `REGION`: Google Cloud region.
- `HOME_DIR`: Home directory path.

Backend Configuration

- `SECRET_KEY`: Secret key for JWT tokens.
- `JWT_ALGORITHM`: Algorithm used for JWT token signing.
- `JWT_EXPIRATION`: Expiration time for JWT tokens.

Webapp Configuration

- `NGROK_AUTH_TOKEN`: Authentication token for Ngrok.
- `NGROK_PORT_MAP`: Port mapping for Ngrok.

Additional Notes
----------------

- Ensure all required environment variables are correctly configured in the `.env` file before starting the application.
- If you encounter issues, review the logs for each service using:

  .. code-block:: bash

     docker compose logs -f [service_name]

Replace `[service_name]` with the name of the service (e.g., `svt-backend`, `svt-postgres`).
