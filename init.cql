-- Create a keyspace (if not exists)
CREATE KEYSPACE IF NOT EXISTS vehicle_db
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

-- Use the keyspace
USE vehicle_db;

-- Create a table having partition key vehicle-id and clustering key is timestamp
CREATE TABLE IF NOT EXISTS vehicle_data (
    vehicle_id text,
    lat double,
    long double,
    speed float,
    temperature float,
    humidity float,
    timestamp timestamp,
    PRIMARY KEY (vehicle_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);