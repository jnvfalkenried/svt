import asyncio
import os

from dotenv import load_dotenv

from consumer import TikTokConsumer, logger

load_dotenv()

rabbitmq_host = os.getenv("RABBITMQ_SERVER")
rabbitmq_port = int(os.getenv("RABBITMQ_PORT"))
rabbitmq_user = os.getenv("RABBITMQ_USER")
rabbitmq_pass = os.getenv("RABBITMQ_PASS")


async def main():
    consumer = TikTokConsumer(
        rabbitmq_host,
        rabbitmq_port,
        rabbitmq_user,
        rabbitmq_pass,
    )

    while True:
        await consumer.initialize()
        if hasattr(consumer, "queue"):
            break

    await consumer.consume_messages()


if __name__ == "__main__":
    logger.info("Starting Consumer")
    asyncio.run(main())
    logger.info("Consumer stopped")
