import datetime
import os
import sys
import requests

import aio_pika
from TikTokApi import TikTokApi

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from helpers.rabbitmq import RabbitMQClient

ms_token = os.environ.get("ms_token", None)


class TikTokProducer(RabbitMQClient):
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = "tiktok_data_producer"
        self.exchange_name = "tiktok_data_exchange"

    async def initialize(self):
        try:
            await self.connect(self.connection_name)
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, type="topic", durable=True
            )
            await self.channel.set_qos(prefetch_count=100)

            print(f"TikTokProducer initialized.")
        except Exception as e:
            print(f"Error while initializing TikTokProducer: {e}")

    async def produce_message(self, key, value):
        try:
            message = aio_pika.Message(
                body=str(value).encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=str(key))
            print(f"Message delivered to {self.exchange} with key {key}")
        except Exception as e:
            print(f"Error producing message: {e}")

    async def get_hashtag_videos(self, hashtag, num_videos=5):
        print(f"Getting videos for hashtag: {hashtag}")
        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[ms_token], num_sessions=1, sleep_after=3
            )
            tag = api.hashtag(name=hashtag)
            async for video in tag.videos(count=num_videos):
                await self.produce_message(
                    key=f"tiktok.hashtag.{hashtag}", value=video.as_dict
                )
        print(f"Finished getting videos for hashtag: {hashtag}")

    async def trending_videos(self, num_videos=5):
        print(f"Getting trending videos")
        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[ms_token], num_sessions=1, sleep_after=3
            )
            async for video in api.trending.videos(count=num_videos):
                await self.produce_message(
                    key=f"tiktok.trending.{datetime.datetime.now()}",
                    value=video.as_dict,
                )
        print(f"Finished getting trending videos")

    async def get_related_videos(self, video_url, num_related_videos=5):
        print(f"Getting related videos for video: {video_url}")
        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[ms_token], num_sessions=1, sleep_after=3
            )
            video = api.video(url=video_url)

            async for related_video in video.related_videos(count=num_related_videos):
                await self.produce_message(
                    key=f"tiktok.related_videos.{video_url}",
                    value=related_video.as_dict,
                )
        print(f"Finished getting related videos for video: {video_url}")

    async def get_video_byters(self, video):
        """
        Get video bytes for a given video url

        Parameters:
        video: TikTokApi.Video containing video url
        """
        s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "range": "bytes=0-",
            "accept-encoding": "identity;q=1, *;q=0",
            "referer": "https://www.tiktok.com/",
        }

        video_url = video.as_dict['video']['bitrateInfo'][0]['PlayAddr']['UrlList'][-1]
        audio_url = video.as_dict['music']['playUrl']

        # Download the video stream
        video_response = s.get(video_url, headers=h)

        if video.as_dict['music']['title'] == "original sound":
            # Download the audio stream
            audio_response = s.get(audio_url, headers=h)

        self.produce_message(
            key=f"video_stream",
            value={
                "video": video_response.content,
                "audio": audio_response.content if video.as_dict['music']['title'] == "original sound" else None
            },
        )