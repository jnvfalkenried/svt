import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
import json
import aio_pika
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from postgresql.database_models import Base, Posts, Authors, Music, Challenges, PostsChallenges
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
rabbitmq_host = os.getenv('RABBITMQ_SERVER')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT'))
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE_PERSISTENT')

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
    authorStats_data = item.get('authorStats', {})
    author = await get_or_create(session, Authors,
        id=author_data.get('id'),
        nickname=author_data.get('nickname'),
        signature=author_data.get('signature'),
        unique_id=author_data.get('uniqueId'),
        verified=author_data.get('verified'),
        digg_count=authorStats_data.get('diggCount'),
        follower_count=authorStats_data.get('followerCount'),
        following_count=authorStats_data.get('followingCount'),
        heart_count=authorStats_data.get('heartCount'),
        video_count=authorStats_data.get('videoCount')
    )

    # Process Music
    music_data = item.get('music', {})
    music = await get_or_create(session, Music,
        id=music_data.get('id'),
        author_name=music_data.get('authorName'),
        title=music_data.get('title'),
        duration=music_data.get('duration'),
        original=music_data.get('original')
    )

    # Process Video
    post = Posts(
        id=item.get('id'),
        created_at=item.get('createTime'),
        description=item.get('desc'),
        duet_enabled=item.get('duetEnabled'),
        duet_from_id=item.get('duetInfo', {}).get('duetFromId'),
        is_ad=item.get('isAd'),
        can_repost=item.get('item_control', {}).get('can_repost'),
        collect_count=item.get('statsV2', {}).get('collectCount'),
        comment_count=item.get('statsV2', {}).get('commentCount'),
        digg_count=item.get('statsV2', {}).get('diggCount'),
        play_count=item.get('statsV2', {}).get('playCount'),
        repost_count=item.get('statsV2', {}).get('repostCount'),
        share_count=item.get('statsV2', {}).get('shareCount'),
        author_id=author.id,
        music_id=music.id
    )
    session.add(post)

    # Process Challenges
    for challenge_data in item.get('challenges', []):
        challenge = await get_or_create(session, Challenges,
            id=challenge_data.get('id'),
            title=challenge_data.get('title'),
            description=challenge_data.get('desc'),
            video_count=challenge_data.get('stats', {}).get('videoCount'),
            view_count=challenge_data.get('stats', {}).get('viewCount')
        )
        posts_challenges = PostsChallenges(post_id=post.id, challenge_id=challenge.id)
        session.add(posts_challenges)

    await session.commit()
    print(f"Processed and stored TikTok data for video ID: {item.get('id', 'Unknown')}")

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        tiktok_data = json.loads(message.body)
        print(" ----------- CONSUMER PRINTING MESSAGE ----------------")
        print(tiktok_data)
        async with AsyncSessionLocal() as session:
            if isinstance(tiktok_data, list):
                print(f"Received a list of {len(tiktok_data)} TikTok data items")
                for item in tiktok_data:
                    await process_tiktok_item(session, item)
            else:
                await process_tiktok_item(session, tiktok_data)

async def main():

    print("------------------------ MY AMAZING PRINT ----------------------------")
    print(f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/")

    connection = await aio_pika.connect_robust(
        f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/"
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.get_queue(rabbitmq_queue)

        print(f"Waiting for messages from queue '{rabbitmq_queue}'. To exit press CTRL+C")

        await queue.consume(process_message)
        
        # Keep the consumer running
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Consumer stopped")