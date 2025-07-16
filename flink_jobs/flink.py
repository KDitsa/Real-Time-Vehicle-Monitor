from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.common.typeinfo import Types
def main():
    # Create Flink environment
    try:
        env = StreamExecutionEnvironment.get_execution_environment()
        t_env = StreamTableEnvironment.create(env)
        env.add_jars(
            f"file:///opt/flink/lib/flink-sql-connector-kafka-3.2.0-1.19.jar"
        )
    except Exception as e:
        print(f"Failed to add jars {e}",flush=True)
    # Define Kafka source
    try:
        print("Connecting to Kafka............")
        t_env.execute_sql("""
            CREATE TABLE kafka_source(
                vehicle_id STRING,
                lat DOUBLE,
                `long` DOUBLE,
                speed DOUBLE,
                temperature DOUBLE,
                humidity DOUBLE,
                `timestamp` STRING
            )WITH(
                'connector' = 'kafka',
                'topic' = 'vehicle_data',
                'properties.bootstrap.servers' = 'kafka:29092',
                'properties.group.id' = 'group1',
                'format' = 'json',
                'scan.startup.mode' = 'earliest-offset'
            )
        """)
        vehicle_type = Types.ROW([
            Types.STRING(),
            Types.DOUBLE(),
            Types.DOUBLE(),
            Types.DOUBLE(),
            Types.DOUBLE(),
            Types.DOUBLE(),
            Types.STRING()
        ])
        vehicle_stream = t_env.to_append_stream(
            t_env.sql_query("SELECT * FROM kafka_source"),
            vehicle_type
        )
        vehicle_stream.print()
        env.execute("Kafka to Flink Job")
        print("Connected to Kafka successfully.")
    except Exception as e:
        print(f"Failed to connect to kafka {e}",flush=True)

if __name__=="__main__":
        main()