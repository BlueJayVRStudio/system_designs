import pika
import time
import os

def callback(ch, method, properties, body):
    print(f"[Worker {os.getpid()}] Received {body.decode()}")
    time.sleep(1.5)  # Simulate processing time
    print(f"[Worker {os.getpid()}] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue='transcode_jobs', durable=True)

# Fair dispatch: don't give more than one unacked message per worker
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='transcode_jobs', on_message_callback=callback)

print(f"[Worker {os.getpid()}] Waiting for jobs...")
channel.start_consuming()
