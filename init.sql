-- enable timescaleDB extension i.e. adds time-series capabilities to PostgreSQL
CREATE EXTENSION IF NOT EXISTS timescaledb;
-- create vehicle_data table if it doesn't already exists
CREATE TABLE IF NOT EXISTS vehicle_data(
    vehicle_id TEXT,
    lat DOUBLE PRECISION,
    long DOUBLE PRECISION,
    speed DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    timestamp TIMESTAMP NOT NULL
    );
-- convert table into hypertable partitioned by timestamp
SELECT create_hypertable('vehicle_data', 'timestamp', if_not_exists => TRUE);