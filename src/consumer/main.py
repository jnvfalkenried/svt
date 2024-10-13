import asyncio
import json
import aio_pika

rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'admin'
rabbitmq_pass = 'admin'
rabbitmq_queue = 'smth'

async def process_tiktok_item(item):
    print(f"Received TikTok data for video ID: {item.get('id', 'Unknown')}")
    print(f"Author: {item.get('author', {}).get('nickname', 'Unknown')}")
    print(f"Description: {item.get('desc', 'No description')}")
    print(f"Hashtags: {[challenge.get('title', '') for challenge in item.get('challenges', [])]}")
    print(f"Music: {item.get('music', {}).get('title', 'Unknown')}")
    print(f"Stats: Views - {item.get('stats', {}).get('playCount', 0)}, Likes - {item.get('stats', {}).get('diggCount', 0)}")
    print("---")

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        tiktok_data = json.loads(message.body)

        if isinstance(tiktok_data, list):
            print(f"Received a list of {len(tiktok_data)} TikTok data items")
            for item in tiktok_data:
                await process_tiktok_item(item)
        else:
            await process_tiktok_item(tiktok_data)

async def main():
    connection = await aio_pika.connect_robust(
        f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/"
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(rabbitmq_queue, durable=True)

        print(f"Waiting for messages from queue '{rabbitmq_queue}'. To exit press CTRL+C")

        await queue.consume(process_message)
        
        # Keep the consumer running
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Consumer stopped")