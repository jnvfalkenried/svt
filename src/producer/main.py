import asyncio
import os
import json
from TikTokApi import TikTokApi

from producer import Producer

HASHTAGS = [
    "election",
    "election2024",
    "trump",
    "harris"
]

async def search_hashtag(producer, hashtag):
    ms_token = os.environ.get("ms_token", None)
    async with TikTokApi() as api:
        try:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=10)
        except Exception as e:
            print(f"Error while creating session: {e}")
            return
        tag = api.hashtag(name=hashtag)
        try:
            async for video in tag.videos(count=5):
                await producer.produce(json.dumps(video.as_dict), "hashtag")
        except Exception as e:
            print(f"Error while searching for videos: {e}")

async def main():
    rabbitmq_server = os.getenv("RABBITMQ_SERVER")
    rabbitmq_port = os.getenv("RABBITMQ_PORT")
    user = os.getenv("RABBITMQ_USER")
    password = os.getenv("RABBITMQ_PASSWORD")

    producers = []

    for _ in HASHTAGS:
        producer = Producer(rabbitmq_server, rabbitmq_port, user, password)
        # Weird way to wait for RabbitMQ to be ready
        while True:
            await producer.initialize()
            if hasattr(producer, "exchange"):
                break
        producers.append(producer)

    search_tasks = [
        search_hashtag(producer, hashtag) for producer, hashtag in zip(producers, HASHTAGS)
    ]

    await asyncio.gather(*search_tasks)

if __name__ == "__main__":
    asyncio.run(main())
