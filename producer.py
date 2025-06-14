import json
import time
import string
import socket
from datetime import datetime
from kafka import KafkaProducer
from config import KAFKA_BROKER, TOPIC_NAME, KAFKA_VERSION
from vehicle_data import generate_vehicle_data

# serialize data: converting to JSON string and encode into bytes
def serializer(message):
    return json.dumps(message).encode('utf-8')
    
def main():
    try:
        vehicle_id = socket.gethostname()
        # creating instance of KafkaProducer class
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            api_version=KAFKA_VERSION,
            value_serializer=serializer
        )
        print('Producer initialized successfully...')
    except Exception as e:
        print(f"Failed to initialize kafka producer {e}",flush=True)
        return
    #send message
    while True:
        send_message = generate_vehicle_data(vehicle_id)
        print(f'Sending message... {datetime.now()} | Message = {str(send_message)}',flush=True)
        future = producer.send(TOPIC_NAME,send_message)
        try:
            record_data = future.get(timeout=10)
            print(f"Message sent to {record_data.topic} partition {record_data.partition} offset {record_data.offset}",flush=True)
        except Exception as e:
            print(f"failed to send message {e}",flush=True)
        time.sleep(60)

if __name__ == "__main__":
    main()