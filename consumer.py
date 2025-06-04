from kafka import KafkaConsumer
import json
import time
from datetime import datetime

from config import KAFKA_BROKER, TOPIC_NAME, GROUP_ID, KAFKA_VERSION

# desrialize data
def deserialize(message):
    return json.loads(message.decode('utf-8'))

# creating instance of KafkaConsumer class
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_BROKER],
    api_version=KAFKA_VERSION,
    auto_offset_reset='earliest',
    value_deserializer=deserialize,
    enable_auto_commit=True,
    group_id=GROUP_ID
)

# print message
while True:
    for message in consumer:
        print(f'Receiving message... {datetime.now()} | Message = {message.value}',flush=True)
    time.sleep(1)