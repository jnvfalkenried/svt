# svt
Project in Cooperation with SVT


## Infra:
alembic for db version control
rabbitmq for queue management
postgresql (pgvector for storing embeddings)


### Alembic commands
- If you want to make changes to database models, add or modify files in [database_models](src/postgresql/database_models/).
- Following this, new migration script can be created using the command
    ```bash
        alembic revision --autogenerate -m "<Insert your message here>"
    ``` 

- The migrations can then be applied using the command:
    ```bash
        alembic upgrade head
    ```

## Code Quality Tools:
To keep your code clean, organized, and easy to maintain, here are some handy tools to consider (first 2 is highly recommended):
* Black: A strict, no-nonsense code formatter for Python that enforces consistent style. (VSCode Extension ID: ms-python.black-formatter)
* isort: Automatically sorts your imports, making them cleaner and easier to read. (VSCode Extension ID: ms-python.isort)
* Pylance: A fast, feature-packed language server for Python that boosts code analysis and autocomplete. (VSCode Extension ID: ms-python.vscode-pylance)
* autoDocstring: A useful extension for automatically generating docstrings for functions, saving you time and improving documentation. (VSCode Extension ID: njpwerner.autodocstring)

## .env skeleton, fill in your values

```env
# RabbitMQ Configuration
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASS=
RABBITMQ_EXCHANGE=
RABBITMQ_HASHTAG_QUEUE=
RABBITMQ_VIDEO_BYTES_QUEUE=
RABBITMQ_EMBEDDINGS_QUEUE=

# PostgreSQL Configuration
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# Other environment variables
HOME_DIR=


This project incorporates certain parts of the TikTok-Api project by David Teather
(https://github.com/davidteather/TikTok-Api), licensed under the MIT License.
The utilized portions include functionality for session creation and TikTok API interactions.
