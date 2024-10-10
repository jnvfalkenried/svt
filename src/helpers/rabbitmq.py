import aio_pika


class RabbitMQClient:
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_port = int(rabbitmq_port)
        self.user = user
        self.password = password
        self.connection = None
        self.channel = None

    async def connect(self, conn_name):
        self.connection = await aio_pika.connect_robust(
            host=self.rabbitmq_server,
            port=self.rabbitmq_port,
            login=self.user,
            password=self.password,
            client_properties={"connection_name": conn_name},
        )
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()
