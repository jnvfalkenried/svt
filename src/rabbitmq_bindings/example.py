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


async def main():
    rabbitmq_exchange = os.getenv("RABBITMQ_EXCHANGE")
    rabbitmq_queue = os.getenv("RABBITMQ_QUEUE_PERSISTENT")

    print("rabbitmq_exchange: ", rabbitmq_exchange)
    print("rabbitmq_queue: ", rabbitmq_queue)

    rabbitmq_client = RabbitMQClient(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD")
    )

    while True:
        try:
            await rabbitmq_client.connect("tiktok_data_exchange")
            break
        except Exception as e:
            # print(f"Error while initializing: {e}")
            pass

    await rabbitmq_client.channel.declare_exchange(
        name=rabbitmq_exchange, type="topic", durable=True
    )
    queue = await rabbitmq_client.channel.declare_queue(
        name=rabbitmq_queue, durable=True
    )
    await queue.bind(exchange=rabbitmq_exchange, routing_key="#")

    print(
        f"Queue {rabbitmq_queue} is now bound to exchange {rabbitmq_exchange} with routing key #"
    )

    await rabbitmq_client.connection.close()


if __name__ == "__main__":
    asyncio.run(main())
