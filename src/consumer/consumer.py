import os
import sys
import asyncio
import json

import aio_pika
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from postgresql.database_models import Base, Posts, Authors, Music, Challenges, PostsChallenges

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from helpers.rabbitmq import RabbitMQClient


class TikTokConsumer(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password, postgres_user, postgres_password, postgres_host, postgres_port, postgres_db):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.input_queue = os.environ.get("RABBITMQ_QUEUE_PERSISTENT")
        self.database_url = (
            f"postgresql+asyncpg://{postgres_user}:{postgres_password}"
            f"@{postgres_host}:{postgres_port}/{postgres_db}"
        )

    async def initialize(self):
        try:
            await self.connect("TikTokConsumer")
            self.queue = await self.channel.get_queue(name=self.input_queue)
            await self.channel.set_qos(prefetch_count=100)

            self.engine = create_async_engine(self.database_url)
            self.AsyncSessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

            print("TikTokConsumer initialized.")
        except Exception as e:
            print(f"Error while initializing: {e}")

    async def consume_messages(self):
        try:
            await self.queue.consume(callback=self.process_message)
            print("Waiting for messages.")
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()
        except Exception as e:
           print(f"Error consuming messages: {e}")

    async def process_message(self, message: aio_pika.IncomingMessage):
        try:
            async with message.process():
                tiktok_data = json.loads(message.body)
                async with self.AsyncSessionLocal() as session:
                    if isinstance(tiktok_data, list):
                        print(f"Received a list of {len(tiktok_data)} TikTok data items")
                        for item in tiktok_data:
                            await self.process_tiktok_item(session, item)
                    else:
                        await self.process_tiktok_item(session, tiktok_data)
        except Exception as e:
            print(f"Error processing message!")
            # print(f"Error processing message: {e}")

    async def get_or_create(self, session, model, **kwargs):
        instance = await session.execute(select(model).filter_by(**kwargs))
        instance = instance.scalar_one_or_none()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            await session.flush()
            return instance

    async def process_tiktok_item(self, session, item):
        # Process Author
        author_data = item.get('author', {})
        author = await self.get_or_create(session, Authors,
            id=author_data.get('id'),
            nickname=author_data.get('nickname'),
            unique_id=author_data.get('uniqueId'),
            signature=author_data.get('signature'),
            verified=author_data.get('verified'),
            stats=author_data.get('stats')
        )

        # Process Music
        music_data = item.get('music', {})
        music = await self.get_or_create(session, Music,
            id=music_data.get('id'),
            title=music_data.get('title'),
            author_name=music_data.get('authorName'),
            duration=music_data.get('duration'),
            original=music_data.get('original')
        )

        # Process Video
        video = Posts(
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
            challenge = await self.get_or_create(session, Challenges,
                id=challenge_data.get('id'),
                title=challenge_data.get('title'),
                desc=challenge_data.get('desc')
            )
            video_challenge = PostsChallenges(video_id=video.id, challenge_id=challenge.id)
            session.add(video_challenge)

        await session.commit()
        print(f"Processed and stored TikTok data for video ID: {item.get('id', 'Unknown')}")