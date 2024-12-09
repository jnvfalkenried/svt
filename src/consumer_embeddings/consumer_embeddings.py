import asyncio
import json
import os
import sys

import aio_pika
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import configure_mappers, sessionmaker

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dotenv import load_dotenv

from helpers.rabbitmq import RabbitMQClient
from postgresql.database_models.video_embeddings import VideoEmbeddings

load_dotenv()


class EmbeddingsConsumer(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = "embeddings_consumer"
        self.exchange_name = os.environ.get("RABBITMQ_EXCHANGE")
        self.input_queue = "embeddings"

        # Initialize database connection using env variables
        db_url = f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
        self.engine = create_async_engine(db_url, echo=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        configure_mappers()

        # Initialize these as None
        self.exchange = None
        self.queue = None
        self.channel = None

    async def initialize(self):
        print("Consumer Embeddings: Initialized")
        try:
            print(
                f"Connecting to RabbitMQ at {self.rabbitmq_server}:{self.rabbitmq_port} with user {self.user}"
            )
            await self.connect(self.connection_name)

            print("Connected to RabbitMQ, declaring exchange...")
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, type="topic", durable=True
            )
            print(f"Declared exchange: {self.exchange_name}")

            self.queue = await self.channel.declare_queue(
                self.input_queue, durable=True
            )
            print(f"Declared queue: {self.input_queue}")

            await self.channel.set_qos(prefetch_count=100)

            print(f"EmbeddingsConsumer initialized successfully")
        except Exception as e:
            print(f"Error initializing EmbeddingsConsumer: {str(e)}")
            raise

    async def get_next_element_id(self, session, post_id):
        # This function gets the highest video embeddings id that exists in the DB, otherwise returns 0
        """Get the next available element_id for a given post_id"""
        result = await session.execute(
            select(func.coalesce(func.max(VideoEmbeddings.element_id), 0)).where(
                VideoEmbeddings.post_id == post_id
            )
        )
        max_element_id = result.scalar()
        return max_element_id + 1

    async def process_tiktok_item(self, session, item, post_id):
        try:
            # Get the next available element_id
            element_id = await self.get_next_element_id(session, post_id)

            embedding = item

            # if (element_id == 1):
            #     # if the next element ID is one, store the description first
            #     embedding = item[1]
            # else:
            #     # Store the video embedding
            #     embedding = item[0]

            print(
                f"Processing embedding for post_id: {post_id}, element_id: {element_id}"
            )

            stmt = (
                insert(VideoEmbeddings)
                .values(
                    post_id=post_id,
                    element_id=element_id,
                    embedding=embedding,
                )
                .on_conflict_do_update(
                    index_elements=[
                        "post_id",
                        "element_id",
                    ],  # As it is Composite primary key
                    set_={"embedding": embedding},
                )
            )

            await session.execute(stmt)
            await session.commit()
            print(f"Inserted embedding for post {post_id} with element_id {element_id}")

        except IntegrityError as e:
            print(f"Integrity error processing message for post {post_id}: {e}")
            await session.rollback()
        except Exception as e:
            print(f"Error processing TikTok item: {e}")
            await session.rollback()
            raise

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
                post_id = message.routing_key.split(".")[-1]
                tiktok_data = json.loads(message.body)

                async with self.async_session() as session:
                    if isinstance(tiktok_data, list):
                        print(
                            f"Received a list of {len(tiktok_data)} TikTok data items"
                        )
                        for item in tiktok_data:
                            await self.process_tiktok_item(session, item, post_id)
                    else:
                        await self.process_tiktok_item(session, tiktok_data, post_id)
        except Exception as e:
            print(f"Error processing message: {e}")


async def main():
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            consumer = EmbeddingsConsumer(
                rabbitmq_server=os.environ["RABBITMQ_HOST"],
                rabbitmq_port=int(os.environ["RABBITMQ_PORT"]),
                user=os.environ["RABBITMQ_USER"],
                password=os.environ["RABBITMQ_PASS"],
            )

            print(
                f"Attempting to initialize consumer (attempt {attempt + 1}/{max_retries})"
            )
            await consumer.initialize()
            await consumer.consume_messages()
            break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                raise


if __name__ == "__main__":
    asyncio.run(main())
