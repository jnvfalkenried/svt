# run with python main.py on producer dir  

# to access db: run psql -h localhost -U admin -d svt


import asyncio
import json
import aio_pika
import os

rabbitmq_host = 'localhost' 
rabbitmq_port = 5672
rabbitmq_user = 'admin'
rabbitmq_pass = 'admin'
rabbitmq_queue = 'smth' 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
json_file_path = os.path.join(grandparent_dir, 'archive', 'elise_response.json')

# Chosen data from the API wrapper
with open(json_file_path, 'r') as file:
    tiktok_data = json.load(file)

async def send_message():
    try:
        connection = await aio_pika.connect_robust(
            f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/"
        )

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(rabbitmq_queue, durable=True)
            message = json.dumps(tiktok_data)
            #print("message: ")
            #print(message)

            # Send msg
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
                routing_key=queue.name,
            )
            print(f"Sent {len(tiktok_data)} TikTok data items to queue: {rabbitmq_queue}")

    except aio_pika.AMQPException as e:
        print(f"Failed to connect to RabbitMQ or send message: {e}")
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from file: {tiktok_data}")
    except FileNotFoundError:
        print(f"File not found: {tiktok_data}")

# Running the async function
asyncio.run(send_message())