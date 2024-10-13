import pika
import json

rabbitmq_host = 'localhost'  # Replace with your RabbitMQ server address
rabbitmq_port = 5672
rabbitmq_user = 'admin'
rabbitmq_pass = 'admin'
rabbitmq_queue = 'smth' 

connection_params = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
)

def process_message(ch, method, properties, body):
    tiktok_data = json.loads(body)

    # Just some prints to start with
    print(f"Received TikTok data for video ID: {tiktok_data['id']}")
    print(f"Author: {tiktok_data['author']['nickname']}")
    print(f"Description: {tiktok_data['desc']}")
    print(f"Hashtags: {[challenge['title'] for challenge in tiktok_data['challenges']]}")
    print(f"Music: {tiktok_data['music']['title']}")
    print(f"Stats: Views - {tiktok_data['stats']['playCount']}, Likes - {tiktok_data['stats']['diggCount']}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# declare queue if it doesnt exist already
channel.queue_declare(queue=rabbitmq_queue, durable=True)

channel.basic_consume(queue=rabbitmq_queue, on_message_callback=process_message)

print(f"Waiting for messages from queue '{rabbitmq_queue}'. To exit press CTRL+C")
channel.start_consuming()