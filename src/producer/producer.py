import aio_pika

from helpers.rabbitmq import RabbitMQClient

class Producer(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)

        print("Producer initialized.")

    async def initialize(self):
        try:
            await self.connect("Producer")
            self.exchange = await self.channel.declare_exchange(
                "tiktok_data_exchange", type="topic", durable=True
            )
            await self.channel.set_qos(prefetch_count=100)
        except Exception as e:
            print(f"Error while initializing: {e}")

    async def produce(self, message, routing_key):
        try:
            message = aio_pika.Message(
                body=message.encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=routing_key)
            print(f"Message sent to {self.exchange} with routing key {routing_key}")
        except Exception as e:
            print(f"Error while producing message: {e}")
