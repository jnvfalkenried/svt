import datetime
import json
import os

import aio_pika

from helpers.rabbitmq import RabbitMQClient
from postgresql.config.db import session
from postgresql.database_scripts.active_hashtags import get_active_hashtags

ms_token = os.environ.get("ms_token", None)


class TasksManager(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = "tasks_manager"
        self.exchange_name = os.environ.get("RMQ_TASKS_EXCHANGE", None)
        self.hashtags_to_monitor = list()

    async def initialize(self):
        try:
            await self.connect(self.connection_name)
            self.exchange = await self.channel.get_exchange(self.exchange_name)
            await self.channel.set_qos(prefetch_count=100)

            print(f"TasksManager initialized.")
        except Exception as e:
            print(f"Error while initializing TasksManager: {e}")

    async def produce_message(self, key, value):
        try:
            message = aio_pika.Message(
                body=value.encode("utf-8") if isinstance(value, str) else value,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=str(key))
            print(f"Message delivered to {self.exchange} with key {key}")
        except Exception as e:
            print(f"Error producing message: {e}")

    async def update_hashtags_to_monitor(self):
        async with session() as s:
            self.hashtags_to_monitor = await get_active_hashtags(s)
            print(f"Hashtags to monitor: {self.hashtags_to_monitor}")

    async def send_tasks_to_queue(self):
        for hashtag in self.hashtags_to_monitor:
            task_data = {
                "hashtag": hashtag,
                "timestamp": datetime.datetime.now().isoformat(),
            }
            await self.produce_message(
                key="producer.hashtag_search", value=json.dumps(task_data)
            )
            print(f"Task sent for hashtag: {hashtag}")
