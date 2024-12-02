import asyncio
from datetime import datetime
import json
import os

import aio_pika

from helpers.logging import setup_logger
from helpers.rabbitmq import RabbitMQClient
from postgresql.config.db import session
from postgresql.database_scripts.authors import insert_author
from postgresql.database_scripts.authors_reporting import insert_author_stats
from postgresql.database_scripts.challenges import insert_or_update_challenge
from postgresql.database_scripts.music import insert_music
from postgresql.database_scripts.posts import insert_post
from postgresql.database_scripts.posts_challenges import insert_post_challenge
from postgresql.database_scripts.posts_reporting import insert_post_stats

logger = setup_logger("consumer")


class TikTokConsumer(RabbitMQClient):
    def __init__(
        self,
        rabbitmq_server,
        rabbitmq_port,
        user,
        password,
    ):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = "tiktok_data_consumer"
        self.input_queue = os.environ.get("RABBITMQ_HASHTAG_QUEUE")

    async def initialize(self):
        try:
            await self.connect(self.connection_name)
            self.queue = await self.channel.get_queue(name=self.input_queue)
            await self.channel.set_qos(prefetch_count=100)

            logger.info(f"Initialized TikTokConsumer")
            logger.debug(
                f"Initialization details: {self.connection_name}, {self.input_queue}"
            )
        except Exception as e:
            logger.error(f"Error initializing TikTokConsumer: {e}")

    async def consume_messages(self):
        try:
            await self.queue.consume(callback=self.process_message)
            logger.info(f"Consuming messages from queue: {self.queue.name}")
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()
        except Exception as e:
            logger.error(f"Error consuming tasks: {e}")

    async def process_message(self, message: aio_pika.IncomingMessage):
        try:
            async with message.process(requeue=True):
                routing_key = message.routing_key
                hashtag = routing_key.split(".")[2]
                tiktok_data = json.loads(message.body.decode("utf-8"))

                logger.info(
                    f"Processing video {tiktok_data.get('id')} for hashtag {hashtag}"
                )

                await self.process_tiktok_item(tiktok_data)
        except Exception as e:
            logger.error(f"Error processing video: {e}")

    async def process_tiktok_item(self, item):
        # Process TikTok item and store in database within a transaction block
        async with session() as s:
            async with s.begin():
                try:
                    # Process Author
                    author_data = item.get("author", {})
                    authorStats_data = item.get("authorStats", {})

                    await insert_author(
                        id=author_data.get("id"),
                        nickname=author_data.get("nickname"),
                        signature=author_data.get("signature"),
                        unique_id=author_data.get("uniqueId"),
                        verified=author_data.get("verified"),
                        session=s,
                    )
                    
                    # Process Author Stats
                    await insert_author_stats(
                        id=author_data.get("id"),
                        collected_at=datetime.fromisoformat(item.get("collected_at")),
                        digg_count=authorStats_data.get("diggCount"),
                        follower_count=authorStats_data.get("followerCount"),
                        following_count=authorStats_data.get("followingCount"),
                        heart_count=authorStats_data.get("heartCount"),
                        video_count=authorStats_data.get("videoCount"),
                        session=s,
                    )

                    # Process Music
                    music_data = item.get("music", {})
                    await insert_music(
                        id=music_data.get("id"),
                        author_name=music_data.get("authorName"),
                        title=music_data.get("title"),
                        duration=music_data.get("duration"),
                        original=music_data.get("original"),
                        session=s,
                    )

                    # Process Video
                    await insert_post(
                        id=item.get("id"),
                        created_at=item.get("createTime"),
                        description=item.get("desc"),
                        duet_enabled=item.get("duetEnabled"),
                        duet_from_id=item.get("duetInfo", {}).get("duetFromId"),
                        is_ad=item.get("isAd"),
                        can_repost=item.get("item_control", {}).get("can_repost"),
                        author_id=author_data.get("id"),
                        music_id=music_data.get("id"),
                        session=s,
                    )

                    # Process Video Stats
                    await insert_post_stats(
                        id=item.get("id"),
                        collected_at=datetime.fromisoformat(item.get("collected_at")),
                        collect_count=item.get("statsV2", {}).get("collectCount"),
                        comment_count=item.get("statsV2", {}).get("commentCount"),
                        digg_count=item.get("statsV2", {}).get("diggCount"),
                        play_count=item.get("statsV2", {}).get("playCount"),
                        repost_count=item.get("statsV2", {}).get("repostCount"),
                        share_count=item.get("statsV2", {}).get("shareCount"),
                        session=s,
                    )

                    # Process Challenges
                    for challenge_data in item.get("challenges", []):
                        await insert_or_update_challenge(
                            id=challenge_data.get("id"),
                            title=challenge_data.get("title"),
                            description=challenge_data.get("desc"),
                            session=s,
                        )

                        await insert_post_challenge(
                            post_id=item.get("id"),
                            challenge_id=challenge_data.get("id"),
                            session=s,
                        )

                    logger.debug(
                        f"Processed and stored TikTok data for video ID: {item.get('id', 'Unknown')}"
                    )

                except Exception as e:
                    logger.error(
                        f"Error in transaction while processing TikTok item, rolling back: {e}"
                    )
                    await s.rollback()
                    raise
