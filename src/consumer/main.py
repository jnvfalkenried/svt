import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
import json
import aio_pika
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.postgresql.alchemy.models import Base, TikTokVideo, Author, Music, Challenge, VideoChallenge
from dotenv import load_dotenv

# run this by python -m src.consumer.main in the root folder


load_dotenv()

# Database setup
DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# RabbitMQ setup
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_user = os.getenv('RABBITMQ_USER', 'admin')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'admin')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'smth')

async def process_tiktok_item(item):
    print("---")
    print(f"Received TikTok data for video ID: {item.get('id', 'Unknown')}")
    print("Some receieved data:") # we receieve the whole json but only print these for now
    print(f"Author: {item.get('author', {}).get('nickname', 'Unknown')}")
    print(f"Description: {item.get('desc', 'No description')}")
    print(f"Hashtags: {[challenge.get('title', '') for challenge in item.get('challenges', [])]}")
    print(f"Music: {item.get('music', {}).get('title', 'Unknown')}")
    #print(f"Stats: Views - {item.get('statsV2', {}).get('playCount', 0)}, Likes - {item.get('statsV2', {}).get('diggCount', 0)}, Comments - {item.get('statsV2', {}).get('commentCount', 0)}")
    print(f"Stats: - {item.get('statsV2', {})}") 
    print("---")

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        tiktok_data = json.loads(message.body)

        if isinstance(tiktok_data, list):
            print(f"Received a list of {len(tiktok_data)} TikTok data items")
            for item in tiktok_data:
                await process_tiktok_item(item)
        else:
            await process_tiktok_item(tiktok_data)

async def main():
    connection = await aio_pika.connect_robust(
        f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/"
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(rabbitmq_queue, durable=True)

        print(f"Waiting for messages from queue '{rabbitmq_queue}'. To exit press CTRL+C")

        await queue.consume(process_message)
        
        # Keep the consumer running
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Consumer stopped")