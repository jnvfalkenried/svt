import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
import json
import aio_pika
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from src.postgresql.alchemy.models import Base, TikTokVideo, Author, Music, Challenge, VideoChallenge
from dotenv import load_dotenv

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

async def get_or_create(session, model, **kwargs):
    instance = await session.execute(select(model).filter_by(**kwargs))
    instance = instance.scalar_one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        await session.flush()
        return instance

async def process_tiktok_item(session, item):
    # Process Author
    author_data = item.get('author', {})
    author = await get_or_create(session, Author,
        id=author_data.get('id'),
        nickname=author_data.get('nickname'),
        unique_id=author_data.get('uniqueId'),
        signature=author_data.get('signature'),
        verified=author_data.get('verified'),
        stats=author_data.get('stats')
    )

    # Process Music
    music_data = item.get('music', {})
    music = await get_or_create(session, Music,
        id=music_data.get('id'),
        title=music_data.get('title'),
        author_name=music_data.get('authorName'),
        duration=music_data.get('duration'),
        original=music_data.get('original')
    )

    # Process Video
    video = TikTokVideo(
        id=item.get('id'),
        desc=item.get('desc'),
        create_time=item.get('createTime'),
        author_id=author.id,
        music_id=music.id,
        stats=item.get('stats')
    )
    session.add(video)

    # Process Challenges
    for challenge_data in item.get('challenges', []):
        challenge = await get_or_create(session, Challenge,
            id=challenge_data.get('id'),
            title=challenge_data.get('title'),
            desc=challenge_data.get('desc')
        )
        video_challenge = VideoChallenge(video_id=video.id, challenge_id=challenge.id)
        session.add(video_challenge)

    await session.commit()
    print(f"Processed and stored TikTok data for video ID: {item.get('id', 'Unknown')}")

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        tiktok_data = json.loads(message.body)
        async with AsyncSessionLocal() as session:
            if isinstance(tiktok_data, list):
                print(f"Received a list of {len(tiktok_data)} TikTok data items")
                for item in tiktok_data:
                    await process_tiktok_item(session, item)
            else:
                await process_tiktok_item(session, tiktok_data)

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