import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='transcode_jobs', durable=True)

for i in range(21):
    msg = f"transcode-job-{i}"
    channel.basic_publish(
        exchange='',
        routing_key='transcode_jobs',
        body=msg.encode(),
        properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
    )
    print(f"Sent: {msg}")
    # time.sleep(0.5)

connection.close()
