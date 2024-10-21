import os
import sys
import asyncio
import cv2
import aio_pika
import vertexai
import json

from scenedetect import SceneManager, AdaptiveDetector, StatsManager, open_video
from typing import Optional
from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
    Video,
    VideoSegmentConfig,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from helpers.rabbitmq import RabbitMQClient


class TikTokVideoProcessor(RabbitMQClient):
    """
    This class is responsible for
    - Extracting key frames from TikTok videos
    - Generating embeddings for the key frames
    """
    def __init__(self, rabbitmq_server, rabbitmq_port, user, password):
        super().__init__(rabbitmq_server, rabbitmq_port, user, password)
        self.connection_name = "tiktok_video_processor"
        self.exchange_name = os.environ.get("RABBITMQ_EXCHANGE")
        self.input_queue = "video_bytes"
        self.google_project_id = os.environ.get("GOOGLE_PROJECT_ID")
        self.region = os.environ.get("REGION")
        self.model = os.environ.get("MODEL")

    async def initialize(self):
        try:
            await self.connect(self.connection_name)
            self.exchange = await self.channel.get_exchange(self.exchange_name)
            self.queue = await self.channel.get_queue(self.input_queue)
            await self.channel.set_qos(prefetch_count=100)

            print(f"TikTokVideoProcessor initialized.")
        except Exception as e:
            print(f"Error while initializing TikTokVideoProcessor: {e}")

    async def produce_message(self, key, value):
        try:
            message = aio_pika.Message(
                body=json.dumps(value).encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await self.exchange.publish(message, routing_key=str(key))
            print(f"Message delivered to {self.exchange} with key {key}")
        except Exception as e:
            print(f"Error producing message: {e}")

    async def consume_messages(self):
        """
        Consume messages from the queue
        """
        try:
            await self.queue.consume(callback=self.message_handler)
            print(f"Waiting for messages from queue: video_bytes")
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()
        except Exception as e:
            print(f"Error consuming message: {e}")

    async def message_handler(self, message: aio_pika.IncomingMessage):
        """
        Handle the incoming message
        """
        try:
            async with message.process(requeue=False):
                body = message.body
                id = message.routing_key.split(".")[-1]
                
                key_frames = await self.extract_key_frames(body)
                embeddings = await self.generate_embeddings(key_frames)
                await self.produce_message(f"tiktok.embeddings.{id}", embeddings)
        except Exception as e:
            print(f"Error processing message: {e}")

    async def extract_key_frames(self, video):
        """
        Extract key frames from the video

        Parameters:
        - video: bytes: The video bytes

        Returns:
        - key_frames: list: The list of key frames
        """

        # Save the video to a temp file
        with open("temp.mp4", "wb") as f:
            f.write(video)

        video = open_video("temp.mp4")
        scene_manager = SceneManager(stats_manager=StatsManager())
        scene_manager.add_detector(
            AdaptiveDetector()
        )
        scene_manager.detect_scenes(video, show_progress=False)  # show_progress=True will the progress of splitting the video
        scene_list = scene_manager.get_scene_list()

        key_frames = []

        cap = cv2.VideoCapture("temp.mp4")
        
        if len(scene_list)== 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            res, frame = cap.read()
            if res:
                key_frames.append(frame)

        for scene in scene_list:
            start_frame = scene[0].get_frames()
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            res, frame = cap.read()
            if res:
                key_frames.append(frame)
        cap.release()

        print(f"Extracted {len(key_frames)} key frames")
        
        # Delete the temp file
        os.remove("temp.mp4")

        return key_frames

    async def generate_embeddings(self, key_frames):
        """
        Generate embeddings for the key frames

        Parameters:
        - key_frames: list: The list of key frames

        Returns:
        - embeddings: list: The list of embeddings
        """
        embeddings_lst = []
        for key_frame in key_frames:
            try:
                embeddings = self.get_image_video_text_embeddings(
                    project_id=self.google_project_id,
                    location=self.region,
                    frame=key_frame,
                    dimension=1408,
                )
                embeddings_lst.append(embeddings)
            except Exception as e:
                print(f"Error generating embeddings: {e}")

                # For testing purposes
                print("Using dummy embeddings")
                embeddings_lst.append([i for i in range(1408)])

        return embeddings_lst
    
    def get_image_video_text_embeddings(
        self,
        project_id: str,
        location: str,
        frame,
        # video_path: str,
        contextual_text: Optional[str] = None,
        dimension: Optional[int] = 1408,
        # video_segment_config: Optional[VideoSegmentConfig] = None,
    ) -> MultiModalEmbeddingResponse:
        """Example of how to generate multimodal embeddings from image, video, and text.

        Args:
            project_id: Google Cloud Project ID, used to initialize vertexai
            location: Google Cloud Region, used to initialize vertexai
            image_path: Path to image (local or Google Cloud Storage) to generate embeddings for.
            video_path: Path to video (local or Google Cloud Storage) to generate embeddings for.
            contextual_text: Text to generate embeddings for.
            dimension: Dimension for the returned embeddings.
                https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings#low-dimension
            video_segment_config: Define specific segments to generate embeddings for.
                https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings#video-best-practices
        """

        cv2.imwrite("temp.jpg", frame)

        vertexai.init(project=project_id, location=location)

        # Check if file exists
        file_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not os.path.exists(file_path):
            print("Google credentials file not found")

        model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
        image = Image.load_from_file("temp.jpg")
        # video = Video.load_from_file(video_path)

        embeddings = model.get_embeddings(
            image=image,
            # video=video,
            # video_segment_config=video_segment_config,
            contextual_text=contextual_text,
            dimension=dimension,
        ).image_embedding

        # Delete the temp file
        os.remove("temp.jpg")

        print(f"Embeddings generated: {len(embeddings)}")

        return embeddings
