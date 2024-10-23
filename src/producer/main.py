import asyncio
import os

from producer import TikTokProducer

HASHTAGS = ["harris"]


async def main():
    producer = TikTokProducer(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD"),
    )

    # await producer.initialize()

    while True:
        await producer.initialize()
        if hasattr(producer, "exchange"):
            break

    await asyncio.gather(
        *(producer.get_hashtag_videos(hashtag) for hashtag in HASHTAGS)
    )


if __name__ == "__main__":
    print("Starting producer")
    asyncio.run(main())
    print("Producer stopped")
