import asyncio
import json
import os

import aio_pika

from helpers.rabbitmq import RabbitMQClient
from postgresql.database_scripts.authors import insert_author
from postgresql.database_scripts.challenges import insert_challenge
from postgresql.database_scripts.music import insert_music
from postgresql.database_scripts.posts import insert_post
from postgresql.database_scripts.posts_challenges import insert_post_challenge
from postgresql.db import session


class TikTokConsumer(RabbitMQClient):
    def __init__(
        self,
        rabbitmq_server,
        rabbitmq_port,
        user,
        password,
    ):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.input_queue = os.environ.get("RABBITMQ_HASHTAG_QUEUE")

    async def initialize(self):
        try:
            await self.connect("TikTokConsumer")
            self.queue = await self.channel.get_queue(name=self.input_queue)
            await self.channel.set_qos(prefetch_count=100)

            print("TikTokConsumer initialized.")
        except Exception as e:
            print(f"Error while initializing: {e}")

    async def consume_messages(self):
        try:
            await self.queue.consume(callback=self.process_message)
            print("Waiting for messages.")
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()
        except Exception as e:
            print(f"Error consuming messages: {e}")

    async def process_message(self, message: aio_pika.IncomingMessage):
        try:
            async with message.process(requeue=True):
                tiktok_data = json.loads(message.body.decode("utf-8"))
                print(f"Processing message: {tiktok_data}")
                await self.process_tiktok_item(tiktok_data)
        except Exception as e:
            print(f"Error processing message: {e}")

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
                        collect_count=item.get("statsV2", {}).get("collectCount"),
                        comment_count=item.get("statsV2", {}).get("commentCount"),
                        digg_count=item.get("statsV2", {}).get("diggCount"),
                        play_count=item.get("statsV2", {}).get("playCount"),
                        repost_count=item.get("statsV2", {}).get("repostCount"),
                        share_count=item.get("statsV2", {}).get("shareCount"),
                        author_id=author_data.get("id"),
                        music_id=music_data.get("id"),
                        session=s,
                    )

                    # Process Challenges
                    for challenge_data in item.get("challenges", []):
                        await insert_challenge(
                            id=challenge_data.get("id"),
                            title=challenge_data.get("title"),
                            description=challenge_data.get("desc"),
                            video_count=challenge_data.get("stats", {}).get(
                                "videoCount"
                            ),
                            view_count=challenge_data.get("stats", {}).get("viewCount"),
                            session=s,
                        )

                        await insert_post_challenge(
                            post_id=item.get("id"),
                            challenge_id=challenge_data.get("id"),
                            session=s,
                        )

                    print(
                        f"Processed and stored TikTok data for video ID: {item.get('id', 'Unknown')}"
                    )

                except Exception as e:
                    print(f"Error in transaction, rolling back: {e}")
                    await s.rollback()
                    raise
