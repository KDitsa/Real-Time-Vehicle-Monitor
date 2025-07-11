from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.common.typeinfo import Types
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions, JdbcExecutionOptions
#from pyflink.formats.json import JsonRowDeserializationSchema


def statement_builder(ps, t):
    ps.setString(1,t[0]),
    ps.setDouble(2,t[1]),
    ps.setDouble(3,t[2]),
    ps.setDouble(4,t[3]),
    ps.setDouble(5,t[4]),
    ps.setDouble(6,t[5]),
    ps.setTimestamp(7,t[6])
def main():
    try:
        # Create Flink environment
        env = StreamExecutionEnvironment.get_execution_environment()
        t_env = StreamTableEnvironment.create(env)
        env.add_jars(
            f"file:///opt/flink/lib/flink-sql-connector-kafka-3.2.0-1.19.jar",
            f"file:///opt/flink/lib/flink-connector-jdbc-3.2.0-1.19.jar"
        )
    except Exception as e:
        print(f"Failed to add jars {e}",flush=True)
    try:
        print("Connecting to Kafka............")
        # Define Kafka source
        t_env.execute_sql("""
            CREATE TABLE kafka_source(
                vehicle_id STRING,
                lat DOUBLE,
                `long` DOUBLE,
                speed DOUBLE,
                temperature DOUBLE,
                humidity DOUBLE,
                `timestamp` TIMESTAMP(3),
                WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
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
            Types.SQL_TIMESTAMP()
        ])
        vehicle_stream = t_env.to_append_stream(
            t_env.sql_query("SELECT * FROM kafka_source"),
            vehicle_type
        )
#        vehicle_stream = vehicle_stream.map(lambda x:(print("Data:",x) or x))
        print("Connected to Kafka successfully.")
    except Exception as e:
        print(f"Failed to connect to kafka {e}",flush=True)

    try:
        print("Connecting to jdbc............")
        # Define TimescaleDB sink table
        jdbc_options = JdbcConnectionOptions.JdbcConnectionOptionsBuilder() \
            .with_url('jdbc:postgresql://timescaledb:5432/vehicle_db') \
            .with_driver_name('org.postgresql.Driver') \
            .with_user_name('postgres') \
            .with_password('password') \
            .build()
#        t_env.execute_sql("""
#            CREATE TABLE vehicle_data(
#                vehicle_id STRING,
#                lat DOUBLE,
#                `long` DOUBLE,
#                speed DOUBLE,
#                temperature DOUBLE,
#                humidity DOUBLE,
#                `timestamp` TIMESTAMP_LTZ(3),
#                WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
#            )WITH(
#                'connector' = 'jdbc',
#                'url' = 'jdbc:postgresql://timescaledb:5432/vehicle_db',
#                'table-name' = 'vehicle_data',
#                'username' = 'postgres',
#                'password' = 'password'
#            )
#        """)
        print("Connected to jdbc successfully.")
    except Exception as e:
        print(f"Failed to connect to jdbc {e}",flush=True)

    try:
        print("Inserting values to TimescaleDB..........")
        # Insert from Kafka to TimescaleDB
#        t_env.execute_sql("""
#            INSERT INTO vehicle_data
#            SELECT * FROM kafka_source
#        """)
        
        vehicle_jdbc_sink = JdbcSink.sink(
            "INSERT INTO vehicle_data (vehicle_id,lat,long,speed,temperature,humidity,timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
            statement_builder,
            JdbcExecutionOptions.builder()
                .with_batch_interval_ms(1)
                .with_batch_size(1)
                .with_max_retries(5)
                .build(),
            jdbc_options
        )
        vehicle_stream.add_sink(vehicle_jdbc_sink)
        env.execute("Vehicle Data Streaming Job")
        print("Inserted Successfully.")
    except Exception as e:
        print(f"Failed to insert to TimescaleDB {e}",flush=True)

if __name__=="__main__":
        main()