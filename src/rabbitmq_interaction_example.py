import asyncio
import csv
import json
import math
from datetime import datetime

import aio_pika
import aiofiles

from src import SUPPORTED_MINER_TYPES, UNIT_NAME, logger
from src.cgminer_api import CGMinerAPI
from helpers.rabbitmq import RabbitMQClient


class Network(RabbitMQClient):
    def __init__(self, EXPORT_PATH, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.export_path = EXPORT_PATH
        self.iprange = []
        self.miners = []

        logger.info(f"Network initialized.")

    async def initialize(self):
        try:
            await self.connect(f"Dispatcher_{UNIT_NAME}")
            self.exchange = await self.channel.declare_exchange(
                "raw_stats_exchange", type="topic", durable=True
            )
            await self.channel.set_qos(prefetch_count=100)
        except Exception as e:
            logger.error(f"Error while initializing: {e}")

    async def update_network(self):
        self.iprange = []
        async with aiofiles.open(self.export_path, "r") as file:
            lines = await file.readlines()
            csv_reader = csv.DictReader(lines)
            for row in csv_reader:
                self.iprange.append(row["Miner_ip"])

        self.miners = [CGMinerAPI(ip) for ip in self.iprange]

        logger.info(f"Network updated with {len(self.miners)} miners.")

    async def check_miner(self, miner):
        logger.debug(f"Checking miner at IP: {miner.host}")

        mq_routing_key = f"{UNIT_NAME}.{miner.host}"
        try:
            miner_version = await miner.send_command("version")
            miner_type = miner_version["VERSION"][0]["Type"]
            if miner_type not in SUPPORTED_MINER_TYPES:
                logger.info(
                    f"Skipping unsupported miner type {miner_type} at {miner.host}"
                )
                return
            stats = await miner.get_processed_stats()
            stats = json.dumps(stats)

            await self.produce_message(mq_routing_key, stats)
            logger.debug(f"Sent stats for {miner.host}")
            print(f"Sent stats for {miner.host}")
        except (asyncio.TimeoutError, Exception) as e:
            logger.error(f"Error on miner {miner.host}: {e}")
            stats = {
                "Elapsed": -1,
                "IP": miner.host,
                "Timestamp": str(math.floor(datetime.now().timestamp() / 10)) + "0",
            }
            stats = json.dumps(stats)
            await self.produce_message(mq_routing_key, stats)
            logger.debug(f"Sent offline stats for {miner.host}")

    async def check_miners(self):
        logger.info("Updating network.")
        await self.update_network()

        logger.info("Initiating check on all miners.")
        await asyncio.gather(*(self.check_miner(miner) for miner in self.miners))
        logger.info("All miners checked successfully.")

    async def produce_message(self, key, value):
        try:
            message = aio_pika.Message(
                body=value.encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=key)
            logger.debug(f"Message delivered to {self.exchange} with key {key}")
        except Exception as e:
            logger.error(f"Error producing message: {e}")
