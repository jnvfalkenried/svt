import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

import asyncio

from dotenv import load_dotenv

from helpers.rabbitmq import RabbitMQClient

load_dotenv()

# RabbitMQ configurations
RMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RMQ_TASKS_EXCHANGE = os.getenv("RMQ_TASKS_EXCHANGE")
RMQ_HASHTAG_QUEUE = os.getenv("RABBITMQ_HASHTAG_QUEUE")
RMQ_VIDEO_BYTES_QUEUE = os.getenv("RABBITMQ_VIDEO_BYTES_QUEUE")
RMQ_EMBEDDINGS_QUEUE = os.getenv("RABBITMQ_EMBEDDINGS_QUEUE")
RMQ_PRODUCER_TASKS_QUEUE = os.getenv("RMQ_PRODUCER_TASKS_QUEUE")


async def main():
    """
    RabbitMQ Queue and Exchange Setup Script

    Sets up a distributed message routing system.

    Exchanges:
        - Main exchange for data processing messages
        - Tasks exchange for producer-related tasks

    Queues:
        - Hashtag queue: TikTok hashtag-related messages
        - Video bytes queue: Raw video byte data
        - Embeddings queue: Video embedding generation messages
        - Producer tasks queue: Producer background tasks

    Routing key patterns:
        - tiktok.hashtag.#: Matches all hashtag-related messages
        - tiktok.bytes.#: Captures video byte-related messages
        - tiktok.embeddings.#: Routes embedding generation messages
        - producer.#: Handles producer task messages
    """
    rabbitmq_client = RabbitMQClient(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD"),
    )

    # Connect to RabbitMQ
    await rabbitmq_client.connect("rmq_bindings")

    # Declare exchanges
    await rabbitmq_client.channel.declare_exchange(
        name=RMQ_EXCHANGE, type="topic", durable=True
    )

    await rabbitmq_client.channel.declare_exchange(
        name=RMQ_TASKS_EXCHANGE, type="topic", durable=True
    )

    # Declare queues
    queue_hashtag = await rabbitmq_client.channel.declare_queue(
        name=RMQ_HASHTAG_QUEUE, durable=True
    )
    await queue_hashtag.bind(exchange=RMQ_EXCHANGE, routing_key="tiktok.hashtag.#")

    print(
        f"Queue {RMQ_HASHTAG_QUEUE} is now bound to exchange {RMQ_EXCHANGE} with routing key: tiktok.hashtag.#"
    )

    queue_video_bytes = await rabbitmq_client.channel.declare_queue(
        name=RMQ_VIDEO_BYTES_QUEUE, durable=True
    )
    await queue_video_bytes.bind(exchange=RMQ_EXCHANGE, routing_key="tiktok.bytes.#")

    print(
        f"Queue {RMQ_VIDEO_BYTES_QUEUE} is now bound to exchange {RMQ_EXCHANGE} with routing key: tiktok.bytes.#"
    )

    queue_embeddings = await rabbitmq_client.channel.declare_queue(
        name=RMQ_EMBEDDINGS_QUEUE, durable=True
    )
    await queue_embeddings.bind(
        exchange=RMQ_EXCHANGE, routing_key="tiktok.embeddings.#"
    )

    print(
        f"Queue {RMQ_EMBEDDINGS_QUEUE} is now bound to exchange {RMQ_EXCHANGE} with routing key: tiktok.embeddings.#"
    )

    producer_tasks_queue = await rabbitmq_client.channel.declare_queue(
        name=RMQ_PRODUCER_TASKS_QUEUE, durable=True
    )
    await producer_tasks_queue.bind(
        exchange=RMQ_TASKS_EXCHANGE, routing_key="producer.#"
    )

    print(
        f"Queue {RMQ_PRODUCER_TASKS_QUEUE} is now bound to exchange {RMQ_TASKS_EXCHANGE} with routing key: producer.#"
    )

    # Close connection
    await rabbitmq_client.connection.close()


if __name__ == "__main__":
    asyncio.run(main())
