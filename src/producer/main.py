import asyncio
import os

from producer import TikTokProducer, logger


async def main():
    producer = TikTokProducer(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD"),
    )

    while True:
        await producer.initialize()
        if hasattr(producer, "exchange"):
            break

    await producer.consume_tasks()


if __name__ == "__main__":
    logger.info("Starting Producer")
    asyncio.run(main())
    logger.info("Producer stopped")
