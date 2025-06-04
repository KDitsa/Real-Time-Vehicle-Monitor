from kafka import KafkaProducer
import json
import time
import random
import string
from datetime import datetime

from config import KAFKA_BROKER, TOPIC_NAME, KAFKA_VERSION

# create random message
def generate_message():
    random_user_id = random.choice(list(range(1,1000)))
    random_recipient_id = random.choice(list(range(1,1000)))
    message = ''.join(random.choices(string.ascii_letters + string.digits,k=50))
    return {
        'user-id': random_user_id,
        'recipient-id': random_recipient_id,
        'message': message
    }

# serialize data: converting to JSON string and encode into bytes
def serializer(message):
    return json.dumps(message).encode('utf-8')
    
# creating instance of KafkaProducer class
# bootstrap_servers parameter identifies kafka broker address that producer will connect to
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    api_version=KAFKA_VERSION,
    value_serializer=serializer
)

#send message
for i in range(6):
    send_message = generate_message()
    print(f'Sending message... {datetime.now()} | Message = {str(send_message)}',flush=True)
    producer.send(TOPIC_NAME,send_message)
    sleep_time = random.randint(1,11)
    time.sleep(sleep_time)
