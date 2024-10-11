import asyncio
import os
from TikTokApi import TikTokApi

from producer import Producer

async def scrape_tiktok_data(producer):
    ms_token = os.environ.get("ms_token", None)
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        async for video in api.trending.videos(count=1):
            await producer.produce(video.as_dict["id"], "hashtag")

async def main():
    rabbitmq_server = os.getenv("RABBITMQ_SERVER")
    rabbitmq_port = os.getenv("RABBITMQ_PORT")
    user = os.getenv("RABBITMQ_USER")
    password = os.getenv("RABBITMQ_PASSWORD")

    producer = Producer(rabbitmq_server, rabbitmq_port, user, password)
    
    # Weird way to wait for RabbitMQ to be ready
    while True:
        await producer.initialize()
        if producer.exchange:
            break

    await scrape_tiktok_data(producer)

if __name__ == "__main__":
    asyncio.run(main())
