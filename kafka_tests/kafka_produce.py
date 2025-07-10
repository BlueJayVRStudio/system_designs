from confluent_kafka import Producer
import time
import random

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    # else:
    #     print(f"Delivered to {msg.topic()} [{msg.partition()}]")

p = Producer({
    'bootstrap.servers': 'localhost:9092',
    'linger.ms': 5,
    'batch.num.messages': 1000
})

message = '0' * 100

t0 = time.perf_counter()

# for j in range(10000):
for j in range(10000):
    for i in range(1000):
        key = str(random.randint(0, 100))
        p.produce(
            'my-topic',
            key=key.encode(),
            value=(f"msg-{key}" + message).encode(),
            callback=delivery_report
        )
        p.poll(0)  # Handle events like acks
    
    if j % 20 == 0:
        p.flush()  # Wait for all messages to be sent
    time.sleep(0.001)

message = '1' * 100
for j in range(1):
    for i in range(1000):
        key = str(random.randint(0, 100))
        p.produce(
            'my-topic',
            key=key.encode(),
            value=(f"msg-{key}" + message).encode(),
            callback=delivery_report
        )
        p.poll(0)  # Handle events like acks
    p.flush()  # Wait for all messages to be sent

print(f"job done, took: {time.perf_counter() - t0} seconds")