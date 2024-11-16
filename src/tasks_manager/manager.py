import datetime
import json
import os

import aio_pika

from helpers.logging import setup_logger
from helpers.rabbitmq import RabbitMQClient
from postgresql.config.db import session
from postgresql.database_scripts.active_hashtags import get_active_hashtags

logger = setup_logger("tasks_manager")


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

            logger.info(f"Initialized TasksManager")
            logger.debug(
                f"Initialization details: {self.connection_name}, {self.exchange_name}"
            )
        except Exception as e:
            logger.error(f"Error initializing TasksManager: {e}")

    async def produce_message(self, key, value):
        try:
            message = aio_pika.Message(
                body=value.encode("utf-8") if isinstance(value, str) else value,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=str(key))
            logger.info(f"Successfully produced message with key: {key}")
            #logger.debug(f"Message details - Key: {key}, Value: {value}")
        except Exception as e:
            logger.error(f"Error producing message: {e}", exc_info=True)
            raise  # Re-raise to let caller handle the error

    async def update_hashtags_to_monitor(self):
        try:
            async with session() as s:
                self.hashtags_to_monitor = await get_active_hashtags(s)
                logger.info(f"Updated hashtags to monitor: {[h.title for h in self.hashtags_to_monitor]}")  # Log just the titles
        except Exception as e:
            logger.error(f"Error updating hashtags to monitor: {e}", exc_info=True)
            self.hashtags_to_monitor = []  # Reset to empty list on error

    async def send_tasks_to_queue(self):
        try:
            for hashtag in self.hashtags_to_monitor:
                task_data = {
                    "hashtag": hashtag.title,  # Use the title attribute instead of the whole object
                    "num_videos": 500,
                    "timestamp": datetime.datetime.now().isoformat(),
                }
                await self.produce_message(
                    key="producer.hashtag_search", 
                    value=json.dumps(task_data)
                )
                logger.info(f"Sent task for hashtag: {hashtag.title}")
        except Exception as e:
            logger.error(f"Error sending tasks to queue: {e}", exc_info=True)
