import json
import time
import random

from datetime import datetime
from datetime import timezone

from itertools import count

from confluent_kafka import Producer
import time

KAFKA_BROKER = "kafka:9092"
TOPIC = "iot-messages"

DEVICE_TYPES = [1, 2, 3, 4, 5]


producer = Producer({"bootstrap.servers": KAFKA_BROKER})


def generate_message() -> dict:
    return {
        "device_id": random.choice(DEVICE_TYPES),
        "event_time": datetime.now().isoformat()[:-3],
        "temperature": round(random.uniform(15, 35), 2),
        "humidity": round(random.uniform(30, 50), 2)
    }


def serialize_message(message: dict) -> bytes:
    return json.dumps(message).encode("utf-8")


def run():
    for _ in count(1, 1):
        message = generate_message()
        producer.produce(topic=TOPIC, value=serialize_message(message))
        time.sleep(1)


if __name__ == "__main__":
    run()
