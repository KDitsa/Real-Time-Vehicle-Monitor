# Weekly report

## Week-1
### Objectives completed
- Set up kafka producer and consumer for vehicle data.
- Created a separate branch timescaleDB-integration to integrate **TimescaleDB** with consumer.
- Integrated **TimescaleDB** to store consumer-processed data.
- Containerized services using **Docker** and managed environments with **Anaconda**.
- Launched **4 producer containers**, each simulating data for one vehicle, to test multi-vehicle data flow.
  
---

### Implementation Summary
- **Producer**: Generates vehicle data: vehicle id, latitude, longitude, speed, temperature, humidity, timestamp.
- **Consumer**: Listens to the topic and inserts data into a TimescaleDB table.
- **TimescaleDB**: Used for time-series data storage.
- **Docker**: Orchestrates kafka, TimescaleDB and application services.
- **Anaconda**: Used for managing python dependencies locally.
- **Branching Strategy**:
  - Initial kafka producer-consumer code was developed on `main` branch.
  - Created `timescaleDB-integration` branch to isolate and implement TimescaleDB integration.
  - Producer and consumer code were modified accordingly in the 'timescaleDB-integration' branch.

---
### Issues faced and Workarounds
#### 1. Docker on Windows
- **Problem**: Docker failed to start on reboot.
- **Workaround**: Switched to **dual-boot with linux** where docker runs reliably.

#### 2. TimescaleDB Slow Startup
- **Problem**: Consumer failed on startup due to database not being ready to accept connection.
- **Workaround**: Added **health check** and set **restart** to `always` in the consumer service configuration. This results in repeated connection attempts until TimescaleDB is ready. **Initial error logs still appear** but do not affect functionality.

#### 3. Resource Cleanup in Docker
- **Problem**: Try-finally and signal handling for graceful shutdown don't execute as expected inside Docker.
- **Status**: Still unresolved. Docker likely terminates processes too quickly for cleanup logic to run. Need deeper investigation.

---

### Closing Notes
This week focused on setting up the core kafka producer-consumer pipeline, integrating TimescaleDB for persistent storage and handling orchestration via Docker. Initial issues aroud Docker behaviour and container dependencies were identified and partially addressed. Further refinements will continue in the upcoming weeks.




## Week-2
### Objectives completed
- Integrated and dockerized **Grafana** with TimescaleDB to visualize vehicle telemetry data and included it in overall orchestration framework.
- Set up **Grafana dashboards** to monitor real-time data ingested via kafka consumer.
- Created a **Grafana contact point using webhook** to send alerts based on specific data threshold.

---

### Implementation Summary
#### Grafana Integration:
- Added Grafana as a Docker service.
- Configured TimescaleDB as a Grafana data source.
- Built dashboards showing various vehicle metrics over time.

#### Alerting Setup:
- Configured alert rules on vehicle metrics.
- Created a **webhook contact point** to send alert data to a local endpoint.

#### Docker Compose File Update
- Extended Docker Compose to include Grafana and handle environment variables and volumes.
- Ensured proper service dependencies (Grafana waits for TimescaleDB).

- **Branching Strategy**:
  - Integrated Grafana within `timescaleDB-integration` branch.
  - After completing all integrations and testing, merged `timescaleDB-integration` back into `main` branch to consolidate changes.

---
### Issues faced and Workarounds
The integration and setup went smoothly without any major issues. Minor challenges were resolved promptly as part of regular testing.

---

### Closing Notes
This week focused on **data visualization and alerting**, enhancing observability of kafka pipeline. The system is now more robust in terms of monitoing and operational visibility. Further refinements will continue in the upcoming weeks.




## Week-3
### Objectives completed
- **Replaced TimescaleDB with Apache Cassandra** as the primary data store for vehicle telemetry data.
- Updated **kafka consumer service to write data into Cassandra** instead of timescaleDB
- Began implementing **data export** functionality for analytics and reporting use cases.
- Studied **Data Lake and Data Warehouse** concepts to better understand long-term data architecture design.

---

### Implementation Summary
#### Cassandra Integration:
- Replaced TimescaleDB with **Apache Cassandra**.
- Refactored database schema and created a new table with
    - **Partition Key**: `vehicle_id`
    - **Clustering Key**: `timestamp` (ordered DESC)
- Replaced init.sql used with TimescaleDB by `init.cql` script
- Introduced a dedicated **cassandra-init service** to:
    - Wait for Cassandra readiness.
    - Check that the target keyspace and table exist before consumer begins writing.

#### Kafka Consumer Update:
- Refactored the consumer logic to support Cassandra integration using the updated schema.
- Ensured full alignment with init.cql definitions, including keyspace and table structure.
- Conducted integration testing with multiple producer containers to validate ingestion across multiple vehicle streams.

#### Branching Strategy:
- Created a new feature branch: **cassandra-migration** to preserve the fully working TimescaleDB implementation on main.
- Made all necessary changes for Cassandra integration within this new branch, ensuring TimescaleDB remains unaffected.

#### Additional Learning & Future Considerations
- Studied the concepts and differences between Data Lakes and Data Warehouses.
- Exploring how these architectures could be integrated to support scalable data storage and advanced analytics.
- Insights gained will inform future decisions on designing robust, long-term data storage and processing solutions.

---

### Issues faced and Workarounds
#### 1. Data Export Failing via Cassandra Exporter
- **Problem:** Attempted to enable metrics/data export using **bitnami/cassandra_exporter** and **criteord/cassandra_exporter**. The exporter frequently fails to start, either:
    - Hangs indefinitely, or
    - Crashes with an error: `Scraper stopped due to uncaught exception: Failed to retrieve RMIServer stub...`
- **Status:** Unresolved. Issue appears related to JMX or RMI misconfiguration within the containerized Cassandra environment. Investigating exporter configurations and possible use of alternative metric exporters or custom scrapers.

#### 2. Cassandra Container Memory Limits
- **Problem:** The Cassandra container was repeatedly crashing due to insufficient memory allocation, especially during initial data ingestion.
- **Workaround:** Increased memory allocation in Docker settings and adjusted Cassandra’s JVM_OPTS to reduce heap usage. System stability has improved post-configuration.

---

### Closing Notes
This week centered on migrating from TimescaleDB to Apache Cassandra, updating the Kafka consumer logic, and laying the groundwork for data export and monitoring. The primary challenge encountered is unstable export functionality due to issues with the Cassandra exporter, which currently hinders reliable data scraping and monitoring.

Despite these challenges, the migration is progressing steadily. Once these export issues are resolved, we plan to integrate Prometheus for metrics collection and Grafana for visualization to fully restore and enhance monitoring capabilities.
