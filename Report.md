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

