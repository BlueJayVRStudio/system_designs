from confluent_kafka import Producer
import time
import uuid


p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

for i in range(3):
    # key = f"user-{i}"
    # key = str(i)
    key = str(uuid.uuid4())  

    p.produce('my-topic', key = key.encode(), value=f"msg-{i}".encode())
    p.flush()
    time.sleep(0.2)