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