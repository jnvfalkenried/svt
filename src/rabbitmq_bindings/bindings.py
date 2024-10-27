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
RMQ_EXCHANGE = "tiktok_data_exchange"
RMQ_HASHTAG_QUEUE = "persistent_queue"
RMQ_VIDEO_BYTES_QUEUE = "video_bytes"
RMQ_EMBEDDINGS_QUEUE = "embeddings"


async def main():
    rabbitmq_client = RabbitMQClient(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD"),
    )

    # Connect to RabbitMQ
    await rabbitmq_client.connect("tiktok_data_exchange")

    # Declare exchange
    await rabbitmq_client.channel.declare_exchange(
        name=RMQ_EXCHANGE, type="topic", durable=True
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

    # Close connection
    await rabbitmq_client.connection.close()


if __name__ == "__main__":
    asyncio.run(main())
