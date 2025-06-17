from kafka import KafkaConsumer
import json
import time
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import datetime
from config import *

# desrialize data
def deserialize(message):
    try:
        return json.loads(message.decode('utf-8'))
    except Exception as e:
        print(f'Deserialization failed: {e}')
        return None
        
def connect_db():
    try:
        cluster = Cluster([DB_HOST], port=DB_PORT)
        session = cluster.connect()
        session.set_keyspace(DB_DATABASE)
        print('Connected to Cassandra successfully')
        return session
    except Exception as e:
        print(f"Failed to connect to Cassandra: {e}", flush=True)
        return None
        
def insert_vehicle_data(session,data):
    try:
        query = """
        INSERT INTO vehicle_data (vehicle_id, lat, long, speed, temperature, humidity, timestamp) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        session.execute(query,(
            data['vehicle_id'],
            data['lat'],
            data['long'],
            data['speed'],
            data['temperature'],
            data['humidity'],
            data['timestamp']
        ))
        print("Inserted successfully.",flush=True)
    except Exception as e:
        print(f"Insertion failed: {e}",flush=True)
        
def main():
    session = connect_db()
    if session is None:
        print('Cannot proceed without Cassandra connection')
        return
    try:
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
        print('Consumer initialized successfully...')
    except Exception as e:
        print(f"Failed to initialize kafka consumer{e}",flush=True)
        return
    try:
        while True:
            print('Listening for messages...')
            for message in consumer:
                data = message.value
                if data:
                    print(f'Receiving message... {datetime.now()} | Topic: {message.topic}, Partition: {message.partition}, Offset:{message.offset} | Message : {data}',flush=True)
                    insert_vehicle_data(session, data)
            sleep(10)
    except KafkaError as e:
        print(f'Kafka error: {e}')
    except Exception as e:
        print(f'Unexpected: {e}')
    finally:
        if session:
            session.shutdown()
        if cluster:
            cluster.shutdown()

if __name__ == "__main__":
    main()