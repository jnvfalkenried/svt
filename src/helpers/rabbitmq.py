import aio_pika


class RabbitMQClient:
    """
    A lightweight asynchronous client for RabbitMQ connections.

    Manages RabbitMQ connection and channel establishment using aio_pika,
    providing a simple interface for creating robust, named connections.

    Attributes:
        rabbitmq_server (str): Hostname or IP address of the RabbitMQ server.
        rabbitmq_port (int): Port number for the RabbitMQ server connection.
        user (str): Username for RabbitMQ authentication.
        connection (aio_pika.Connection): Established RabbitMQ connection.
        channel (aio_pika.Channel): Active communication channel for the connection.
    """
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        """
        Initialize the RabbitMQ client with connection parameters.

        Args:
            rabbitmq_server (str): Server address for the RabbitMQ instance.
            rabbitmq_port (str or int): Port number for RabbitMQ connection.
            user (str): Authentication username.
            password (str): Authentication password.
        """
        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_port = int(rabbitmq_port)
        self.user = user
        self.password = password
        self.connection = None
        self.channel = None

    async def connect(self, conn_name):
        """
        Establish a robust connection to the RabbitMQ server.

        Creates an asynchronous connection with a specified connection name,
        initializing both connection and channel for further operations.

        Args:
            conn_name (str): A unique name to identify the connection,
                             useful for monitoring and debugging.

        Raises:
            aio_pika.exceptions.AMQPConnectionError: If connection fails.
        """
        self.connection = await aio_pika.connect_robust(
            host=self.rabbitmq_server,
            port=self.rabbitmq_port,
            login=self.user,
            password=self.password,
            client_properties={"connection_name": conn_name},
        )
        self.channel = await self.connection.channel()

    async def close(self):
        """
        Gracefully close the existing RabbitMQ connection.

        Safely terminates the connection if one exists. No-op if no 
        connection is active. Helps prevent resource leaks and ensures
        clean shutdown of RabbitMQ connections.
     """
        if self.connection:
            await self.connection.close()
