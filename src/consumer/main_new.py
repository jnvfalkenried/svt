import os
import asyncio

from dotenv import load_dotenv
from consumer import TikTokConsumer

load_dotenv()

rabbitmq_host = os.getenv('RABBITMQ_SERVER')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT'))
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE_PERSISTENT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_pass = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_db = os.getenv('POSTGRES_DB')

async def main():
    consumer = TikTokConsumer(
        rabbitmq_host,
        rabbitmq_port,
        rabbitmq_user,
        rabbitmq_pass,
        postgres_user,
        postgres_pass,
        postgres_host,
        postgres_port,
        postgres_db
    )

    while True:
        await consumer.initialize()
        if hasattr(consumer, 'queue'):
            break

    await consumer.consume_messages()

if __name__ == "__main__":
    print("Starting consumer")
    asyncio.run(main())
    print("Consumer stopped")