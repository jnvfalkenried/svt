import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

import asyncio

from dotenv import load_dotenv

from src.helpers.rabbitmq import RabbitMQClient

load_dotenv()


async def main():
    rabbitmq_alert_events_exchange = "alert_events_exchange"
    rabbitmq_alert_events_queue = "alert_events_queue"

    rabbitmq_client = RabbitMQClient(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD"),
    )

    await rabbitmq_client.connect("bindings_alert_events_exchange")

    await rabbitmq_client.channel.declare_exchange(
        name=rabbitmq_alert_events_exchange, type="topic", durable=True
    )
    queue = await rabbitmq_client.channel.declare_queue(
        name=rabbitmq_alert_events_queue, durable=True
    )
    await queue.bind(exchange=rabbitmq_alert_events_exchange, routing_key="#")

    print(
        f"Queue {rabbitmq_alert_events_queue} is now bound to exchange {rabbitmq_alert_events_exchange} with routing key #"
    )

    await rabbitmq_client.connection.close()


if __name__ == "__main__":
    asyncio.run(main())
