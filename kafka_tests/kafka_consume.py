from confluent_kafka import Consumer
import time
import os

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'debug-consumer-group-1',  
    'enable.auto.commit': False,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

def on_assign(consumer, partitions):
    print(f"[PID {os.getpid()}] Assigned partitions: {partitions}")

consumer.subscribe(['my-topic'], on_assign=on_assign)

print(f"[PID {os.getpid()}] Waiting for messages...")

try:
    while True:
        # msg = consumer.poll(1.0)
        messages = consumer.consume(num_messages=100)

        for msg in messages:
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue

            print(f"[PID {os.getpid()}] Received from partition {msg.partition()}: {msg.value().decode('utf-8')}")
            # time.sleep(10)  # Simulate processing delay
        if messages:
            consumer.commit(asynchronous=True)
except KeyboardInterrupt:
    print("Exiting")
finally:
    consumer.close()