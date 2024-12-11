import asyncio
import json
import os
import pickle
import socket
from datetime import datetime

import aio_pika
import requests
from TikTokApi import TikTokApi

from helpers.logging import setup_logger
from helpers.rabbitmq import RabbitMQClient

# Get the hostname (e.g., producer.1, producer.2)
hostname = socket.gethostname()

# Extract replica number from hostname
replica_number = hostname.split(".")[-1]

logger = setup_logger(f"producer_{replica_number}")


class TikTokProducer(RabbitMQClient):
    """
    TikTokProducer class to produce TikTok data to RabbitMQ.
    
    It can produce messages to the exchange and consume tasks from the tasks queue.

    Attributes:
        connection_name (str): The connection name for the RabbitMQ connection.
        exchange_name (str): The exchange name for the RabbitMQ exchange.
        tasks_queue (str): The tasks queue name for the RabbitMQ tasks queue.
    """
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        """
        Initialize the TikTokProducer with RabbitMQ connection details.

        Args:
            rabbitmq_server (str): The RabbitMQ server hostname.
            rabbitmq_port (int): The RabbitMQ server port.
            user (str): The RabbitMQ server username.
            password (str): The RabbitMQ server password.
        """
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = f"tiktok_data_producer_{replica_number}"
        self.exchange_name = os.environ.get("RABBITMQ_EXCHANGE")
        self.tasks_queue = os.environ.get("RMQ_PRODUCER_TASKS_QUEUE")
        self.semaphore = asyncio.Semaphore(1)  # Allow only 1 task at a time

    async def initialize(self):
        """
        Initialize the TikTokProducer by connecting to RabbitMQ and setting up the exchange and tasks queue.
        """
        try:
            await self.connect(self.connection_name)
            self.exchange = await self.channel.get_exchange(self.exchange_name)
            self.tasks_queue = await self.channel.get_queue(name=self.tasks_queue)
            # Get only 1 message at a time
            await self.channel.set_qos(prefetch_count=1)

            logger.info(f"Initialized TikTokProducer")
            logger.debug(
                f"Initialization details: {self.connection_name}, {self.exchange_name}, {self.tasks_queue}"
            )
        except Exception as e:
            logger.error(f"Error initializing TikTokProducer: {e}")

    async def produce_message(self, key, value):
        """
        Produce a message to the exchange with the given key and value.

        Args:
            key (str): The routing key for the message.
            value (str): The message value.
        """
        try:
            message = aio_pika.Message(
                body=value.encode("utf-8") if isinstance(value, str) else value,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=str(key))
            # logger.debug(
            #     f"Produced message with key: {key} \n Message details: {key}: {value}"
            # )
        except Exception as e:
            logger.error(f"Error producing message: {e}")

    async def consume_tasks(self):
        """
        Consume tasks from the tasks queue and process them.
        """
        try:
            await self.tasks_queue.consume(callback=self.process_tasks)
            logger.info(f"Consuming tasks from queue: {self.tasks_queue.name}")
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()
        except Exception as e:
            logger.error(f"Error consuming tasks: {e}")

    async def process_tasks(self, message: aio_pika.IncomingMessage):
        """
        Process the incoming task from the tasks queue.

        Args:
            message (aio_pika.IncomingMessage): The incoming task from the tasks queue.
        """
        async with self.semaphore:  # Ensure only one task runs at a time
            try:
                async with message.process(requeue=True):
                    routing_key = message.routing_key
                    task_type = routing_key.split(".")[1]
                    task_params = json.loads(message.body.decode("utf-8"))

                    logger.info(f"Processing {task_type} task: {task_params}")

                    if task_type == "hashtag_search":
                        await self.get_hashtag_videos(
                            hashtag=task_params["hashtag"],
                            num_videos=task_params["num_videos"],
                            scheduled_at=task_params["timestamp"],
                        )
            except Exception as e:
                logger.error(
                    f"Error {e} occurred while processing task {task_params}. Rescheduling!"
                )

    async def get_hashtag_videos(self, hashtag, scheduled_at, num_videos=5):
        """
        Get videos for a given hashtag and produce them to the exchange.

        Args:
            hashtag (str): The hashtag to search for.
            scheduled_at (str): The scheduled time to collect the videos.
            num_videos (int): The number of videos to collect.
        """
        logger.info(f"Getting {num_videos} videos for hashtag: {hashtag}")

        # Round scheduled_at to minutes
        collected_at = datetime.fromisoformat(scheduled_at).replace(
            second=0, microsecond=0
        )

        async with TikTokApi() as api:
            await api.create_sessions(num_sessions=1, sleep_after=3)

            await asyncio.sleep(1)

            tag = api.hashtag(name=hashtag)
            async for video in tag.videos(count=num_videos):
                video_dict = video.as_dict
                await self.produce_message(
                    key=f"tiktok.hashtag.{hashtag}",
                    value=json.dumps(
                        {
                            **video_dict,
                            "collected_at": collected_at.isoformat(),
                        }
                    ),
                )

                await self.get_video_bytes(video)
        logger.info(f"Finished getting videos for hashtag: {hashtag}")

    async def get_video_bytes(self, video):
        """
        Get the video bytes for the given video and produce them to the exchange.

        Args:
            video (dict): The TikTok video dictionary object.
        """
        try:
            s = requests.Session()
            h = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "range": "bytes=0-",
                "accept-encoding": "identity;q=1, *;q=0",
                "referer": "https://www.tiktok.com/",
            }

            video_url = video.as_dict["video"]["bitrateInfo"][0]["PlayAddr"]["UrlList"][
                -1
            ]
            audio_url = video.as_dict["music"]["playUrl"]

            # Download the video stream
            video_response = s.get(video_url, headers=h)

            # Don't download the audio stream if it is music because of copyright issues
            if video.as_dict["music"]["title"] == "original sound":
                # Download the audio stream
                audio_response = s.get(audio_url, headers=h)

            body = pickle.dumps(
                {
                    "video": video_response.content,
                    # "audio": audio_response.content,
                    "description": video.as_dict["desc"],
                }
            )
        except Exception as e:
            logger.error(
                f"Error getting video bytes: {e} for video: \n {video.as_dict}"
            )
            return

        await self.produce_message(
            key=f"tiktok.bytes.{video.as_dict['id']}",
            # For now we are only sending the video bytes
            value=body,
        )
