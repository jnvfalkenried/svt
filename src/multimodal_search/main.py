import asyncio
import os

from multimodal_search_processor import TikTokVideoProcessor

async def main():
    processor = TikTokVideoProcessor(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASS"),
    )

    while True:
        await processor.initialize()
        if hasattr(processor, "queue"):
            break

    await processor.consume_messages()

if __name__ == "__main__":
    print("Starting Multimodal Search Processor")
    asyncio.run(main())
    print("Processor stopped")
