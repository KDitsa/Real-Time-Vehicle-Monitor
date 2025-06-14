from kafka import KafkaConsumer
import json
import time
import psycopg2
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
        conn = psycopg2.connect(
            host = DB_HOST,
            port = DB_PORT, 
            user = DB_USER, 
            password = DB_PASSWORD, 
            dbname = DB_DATABASE
        )
        conn.autocommit = True
        print('Connected to timescaleDB successfully')
        return conn
    except Exception as e:
        print(f"Failed to connect to timescaleDB {e}",flush=True)
        return None
        
def insert_vehicle_data(cur,data):
    try:
        cur.execute(
            "INSERT INTO vehicle_data (vehicle_id, lat, long, speed, temperature, humidity, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                data['vehicle_id'],
                data['lat'],
                data['long'],
                data['speed'],
                data['temperature'],
                data['humidity'],
                data['timestamp']
            )
        )
        print("Inserted successfully.",flush=True)
    except Exception as e:
        print(f"Insertion failed: {e}",flush=True)

def show_vehicle_data(cur,limit=5):
    try:
        cur.execute("SELECT * FROM vehicle_data ORDER BY timestamp DESC LIMIT %s",(limit,))
        rows = cur.fetchall()
        print("\n Latest entries:")
        for row in rows:
            print (row)
        print("-"*50)
    except Exception as e:
        print(f"Error while fetching entries: {e}",flush=True)

def main():
    db_conn = connect_db()
    if db_conn is None:
        print('Cannot create table. No database connection')
        return
    cur = db_conn.cursor()
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
                    insert_vehicle_data(cur,data)
                    show_vehicle_data(cur)
            sleep(10)
    except KafkaError as e:
        print(f'Kafka error: {e}')
    except Exception as e:
        print(f'Unexpected: {e}')
    finally:
        if db_conn:
            db_conn.close()

if __name__ == "__main__":
    main()