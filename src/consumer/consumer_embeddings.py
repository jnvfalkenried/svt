import os
import sys
import json
import asyncio
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import aio_pika

from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from helpers.rabbitmq import RabbitMQClient
from postgresql.database_models.video_embeddings import VideoEmbeddings

from dotenv import load_dotenv
load_dotenv()

class EmbeddingsConsumer(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = "embeddings_consumer"
        self.exchange_name = os.environ.get("RABBITMQ_EXCHANGE")
        #self.input_queue = "video_embeddings_queue"  # Changed queue name
        self.input_queue = "embeddings"  # Changed queue name
        #self.routing_key = "tiktok.embeddings.*"
        
        # Initialize database connection using env variables
        db_url = f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
        self.engine = create_async_engine(db_url, echo=True)
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Initialize these as None
        self.exchange = None
        self.queue = None
        self.channel = None

    async def initialize(self):
        try:
            print(f"Connecting to RabbitMQ at {self.rabbitmq_server}:{self.rabbitmq_port} with user {self.user}")
            await self.connect(self.connection_name)
            
            print("Connected to RabbitMQ, declaring exchange...")
            # Declare the exchange instead of getting it
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name,
                type="topic",  # Use topic exchange for pattern matching
                durable=True
            )
            print(f"Declared exchange: {self.exchange_name}")
            
            # Declare the queue and bind it to the exchange
            self.queue = await self.channel.declare_queue(
                self.input_queue,
                durable=True
            )
            print(f"Declared queue: {self.input_queue}")
            
            await self.channel.set_qos(prefetch_count=100)
            
            print(f"EmbeddingsConsumer initialized successfully")
        except Exception as e:
            print(f"Error initializing EmbeddingsConsumer: {str(e)}")
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

    async def process_tiktok_item(self, session, item, id):
        print("post id: ", id)
        print("item: ", item)
        try:
            video_embedding = item[0]
            description_embedding = item[1]

            stmt = insert(VideoEmbeddings).values(
                    id=id,
                    embedding=video_embedding,
                    description_embedding=description_embedding,
                ).on_conflict_do_update(
                    index_elements=['id'],  # Conflict based on the primary key (id)
                    set_={
                        "video_embedding": video_embedding,
                        "description_embedding": description_embedding,
                        "description": "Generated from video keyframe",
                        "updated_at": func.now()
                    }
                )

            await session.execute(stmt)
                
            # Commit the transaction
            await session.commit()
            print(f"Upserted {len(item['embeddings'])} embeddings for post {id}")

        except IntegrityError as e:
            print(f"Integrity error processing message for post {id}: {e}")
        except Exception as e:
            print(f"Error processing TikTok item: {e}")

    async def process_message(self, message: aio_pika.IncomingMessage):
        try:
            async with message.process():
                id = message.routing_key.split(".")[-1]
                tiktok_data = json.loads(message.body)
                async with self.async_session() as session:
                    if isinstance(tiktok_data, list):
                        print(f"Received a list of {len(tiktok_data)} TikTok data items")
                        for item in tiktok_data:
                            await self.process_tiktok_item(session, item, id)
                    else:
                        await self.process_tiktok_item(session, tiktok_data, id)
        except Exception as e:
            print(f"Error processing message: {e}")

async def main():
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            consumer = EmbeddingsConsumer(
                rabbitmq_server=os.environ['RABBITMQ_HOST'],  # Use square brackets to raise KeyError if not found
                rabbitmq_port=int(os.environ['RABBITMQ_PORT']),
                user=os.environ['RABBITMQ_USER'],
                password=os.environ['RABBITMQ_PASS']
            )
            
            print(f"Attempting to initialize consumer (attempt {attempt + 1}/{max_retries})")
            await consumer.initialize()
            await consumer.consume_messages()
            break  # If we get here, everything worked
            
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