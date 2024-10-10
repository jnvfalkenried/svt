import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

import asyncio
import json
import traceback

import aio_pika

from src.helpers.logging import logger
from src.helpers.postgresql.scripts import get_monitor_settings
from src.helpers.rabbitmq import RabbitMQClient


class RabbitMQMinerStatsHandler(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.input_queue = "raw_stats_queue"
        self.output_exchange = "alert_events_exchange"

    async def initialize(self):
        try:
            await self.connect("RabbitMQMinerStatsHandler")
            self.queue = await self.channel.declare_queue(
                name=self.input_queue, durable=True
            )
            self.exchange = await self.channel.declare_exchange(
                name=self.output_exchange, type="topic", durable=True
            )
            await self.channel.set_qos(prefetch_count=100)
        except Exception as e:
            logger.error(f"Error while initializing: {e}\n{traceback.format_exc()}")

    async def consume_messages(self):
        try:
            await self.queue.consume(callback=self.process_message)
            logger.info("Waiting for messages.")
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()
        except Exception as e:
            logger.error(f"Error consuming messages: {e}\n{traceback.format_exc()}")

    async def process_message(
        self, message: aio_pika.abc.AbstractIncomingMessage
    ) -> None:
        try:
            async with message.process(requeue=True):
                client_id = message.routing_key.split(".")[0]
                stats = json.loads(message.body.decode("utf-8"))
                logger.debug(f"Client ID: {client_id}; Miner stats: {stats}")
                await self.categorize_message(client_id, stats)
        except Exception as e:
            logger.error(f"Error processing message: {e}\n{traceback.format_exc()}")

    async def categorize_message(self, client_id, stats):
        stats_request_timeout = 60.0
        try:
            if stats["Elapsed"] == "No data":
                msg_key = f"{client_id} | Restart"
            elif stats["Elapsed"] < 0:
                msg_key = f"{client_id} | Offline"
            else:
                monitor_settings = await get_monitor_settings(
                    client_id, stats["MinerType"]
                )
                MAX_ALLOWED_TEMP = int(monitor_settings["max_allowed_temp"])
                MIN_ALLOWED_FAN_SPEED = int(monitor_settings["min_allowed_fan_speed"])
                MAX_ALLOWED_FAN_SPEED = int(monitor_settings["max_allowed_fan_speed"])
                MAX_ALLOWED_HASHRATE_REDUCTION = (
                    int(monitor_settings["max_allowed_hashrate_reduction"]) / 100
                )

                max_temp, fan_speeds = await self._parse_temps_and_fans(stats)

                if (
                    stats["Elapsed"] > 0
                    and stats["Elapsed"] < 1.2 * stats_request_timeout
                ):
                    msg_key = f"{client_id} | Restart"
                elif max_temp > MAX_ALLOWED_TEMP:
                    msg_key = f"{client_id} | Temperature"
                elif stats["FanNum"] < 4 or any(
                    fan <= MIN_ALLOWED_FAN_SPEED or fan >= MAX_ALLOWED_FAN_SPEED
                    for fan in fan_speeds
                ):
                    msg_key = f"{client_id} | Fan"
                elif (
                    stats["GHS_RT"]
                    < (1 - MAX_ALLOWED_HASHRATE_REDUCTION) * stats["IdealGHS"]
                ):
                    msg_key = f"{client_id} | Hashrate"
                else:
                    msg_key = None
                    logger.debug(
                        f"Client ID: {client_id}; Miner {stats['IP']} is operating normally."
                    )

            if msg_key:
                stats_json = json.dumps(stats)
                await self.produce_message(msg_key, stats_json)
        except Exception as e:
            logger.error(f"Error categorizing message: {e}\n{traceback.format_exc()}")

    async def produce_message(self, key, value):
        try:
            message = aio_pika.Message(
                body=value.encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=key)
            logger.debug(f"Message delivered to {self.output_exchange} with key {key}")
        except Exception as e:
            logger.error(f"Error producing message: {e}\n{traceback.format_exc()}")

    async def _parse_temps_and_fans(self, stats):
        try:
            max_temp = max(
                [int(temp) for temp in stats["TempIn"].replace("None", "0").split("/")]
                + [
                    int(temp)
                    for temp in stats["TempOut"].replace("None", "0").split("/")
                ]
            )
            fan_speeds = [
                int(speed)
                for speed in stats["FanSpeed"].replace("None", "0").split("/")
            ]
        except ValueError as e:
            logger.error(f"Error parsing stats: {stats}. Error: {e}")
            max_temp = 0
            fan_speeds = [0]
        return max_temp, fan_speeds
