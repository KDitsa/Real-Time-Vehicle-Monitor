# 🚘 Real-Time Vehicle Telemetry Monitoring System
## 📘 Overview
This project implements a real-time vehicle telemetry monitoring system that ingests, stores, visualizes, and monitors data streams from multiple simulated vehicles. It is built using Kafka, Apache Cassandra, and Prometheus, all orchestrated through Docker. The goal is to simulate real-world IoT telemetry workflows with observability, alerting, and scalability in mind.

## 🎯 Motivation
In a world of connected vehicles and intelligent transportation systems, real-time telemetry is critical for performance monitoring, predictive maintenance, and safety analysis. This project explores how modern data pipelines and observability stacks can be leveraged to handle high-throughput vehicle data reliably and efficiently.

## ⚙️ Getting Started

This project is fully containerized and requires only Docker for setup and execution.

### ✅ Requirements
- **Docker** (with Docker Compose support)  
  [→ Install Docker](https://docs.docker.com/get-docker/)

> All components — Kafka, Cassandra, Prometheus, and Python/Java services—are managed using Docker Compose. No manual installation of individual dependencies is necessary.

---

### 🚀 Running the System

```bash
# Clone the repository
git clone --single-branch --branch cassandra-migration https://github.com/KDitsa/Real-Time_Vehicle-Monitor.git
cd Real-Time_Vehicle-Monitor

# Build and launch all services
docker-compose up --build
```
Once initialized:
- Kafka producers begin simulating and publishing vehicle telemetry data.
- The consumer ingests this data and stores it in Apache Cassandra.
- Prometheus starts scraping metrics from exporters and Java applications via the Java Agent.

> Note: The initial startup may take 1–2 minutes while services pass their health checks and dependencies initialize.

---

### 🧹 Stopping and Cleanup

To stop all running services:
```bash
docker-compose down
```
To remove all associated containers, networks, and volumes:

```bash
docker-compose down -v
```

## 🖥️ System Architecture
The system consists of five major components:
1. **Kafka Producers** – Simulate telemetry data for each vehicle.
2. **Kafka Consumer** – Processes and forwards incoming data to TimescaleDB.
3. **Apache Cassandra** – Distributed, scalable NoSQL database for time-series-style telemetry data.
4. **Prometheus Exporter (Java Agent)** – A JMX-based exporter installed on Cassandra to expose JVM metrics such as heap memory usage, process cpu load, complete tasks, live data size and so on.
5. **Prometheus** – Scrapes and visualizes system and application metrics for monitoring with the help of exporter.
6. **Docker** – Handles the orchestration of all services.

## 🔄 Data Flow Summary
Vehicle Simulation (Producer) --> Kafka Topic --> Kafka Consumer --> Cassandra --> Exporter --> Prometheus 

## 🛠️ Implementation Journey
### 🚗 Simulating Vehicles with Kafka Producers
The journey began with the design of a Kafka-based producer-consumer pipeline tailored to vehicle telemetry. Each producer simulates a vehicle sending real-time data including:
- `vehicle_id`: Unique identifier for the vehicle
- `latitude`, `longitude`: GPS coordinates for real-time location tracking
- `speed`: Vehicle’s current speed in km/h
- `temperature`, `humidity`: Engine metrics
- `timestamp`: UTC timestamp of data generation

Kafka producers were containerized using Docker, with four separate containers representing individual vehicles. These containers emit telemetry data into a Kafka topic, forming the first stage of the data pipeline.

---

### 📥 Real-Time Ingestion – Kafka Consumer
A Python-based Kafka consumer subscribes to the same topic and continuously listens for incoming messages. On message receipt, it:
- Parses the incoming JSON payload
- Stores it into a Cassandra table using an optimized schema for querying by vehicle and time range

Cassandra is well-suited for scalable and distributed write-heavy telemetry workloads.

---

### 💾 Storage with Apache Cassandra
Apache Cassandra provides:

- High availability with no single point of failure
- Linear scalability for write-heavy telemetry workloads
- A flexible schema to store time-series vehicle data efficiently

Cassandra’s distributed architecture makes it ideal for high-ingest, geographically distributed deployments.

---

### 📈 Metrics Scraping with Prometheus and Java Agent
Prometheus is configured to:
- Scrape JVM-level metrics (e.g. heap memory usage, garbage collection, thread activity) from Apache Cassandra using the Prometheus JMX Java Agent.
- Monitor the health and performance of core infrastructure components like Cassandra.

The Prometheus Java Agent is installed during Docker image builds using `wget` and `maven`. The agent exposes application metrics at a `/metrics` endpoint, which Prometheus regularly scrapes.

---

### 🌿 Isolated Development with Git Branching
To ensure clean and modular development, the integration with Apache Cassandra and Prometheus was carried out in a dedicated Git branch: `cassandra-migration`. This isolated environment allowed for iterative testing and adjustments without disrupting the main codebase.

---

### 🐳 Orchestration with Docker
All services — Kafka, Zookeeper, Cassandra, Prometheus, producer(s), and consumer — are defined and orchestrated in a single docker-compose.yaml file. A key challenge in orchestrating interdependent services is ensuring correct startup order. To address this, a series of Docker health checks and service dependencies were implemented, allowing containers to wait for their critical dependencies before becoming active.
- **Zookeeper** acts as the foundational coordination service for Kafka. It exposes a health check that verifies responsiveness by sending a `ruok` command and expecting an `imok` response. Kafka explicitly depends on Zookeeper and waits until Zookeeper is healthy before starting.
- **Kafka** depends on Zookeeper and performs its own health check by attempting to list Kafka topics. This ensures Kafka is fully operational and ready to accept connections before producers and consumers start.
- The **producer containers** simulate vehicle telemetry data and depend on Kafka's health status. Each producer waits until Kafka is healthy before publishing messages.
- The **consumer container**, which subscribes to Kafka topics and inserts data into Cassandra, waits on **both Kafka and Apache Cassandra** services. Cassandra exposes a health check using `describe keyspaces` to confirm the keyspace is ready before the consumer starts processing data.
- **Cassandra-init** depends on cassandra and mounts volume for init.cql to run and create the required keyspace vehicle_db.
- **Prometheus** depends on Cassandra being healthy before launching, ensuring keyspace loads correctly.

---

## ⚠️ Challenges Encountered

| Issue                    | Description                                                                                     | Resolution                                                                                             |
|--------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Docker on Windows        | Services failed to start reliably after system reboots.                                         | Switched to a Linux environment for more stable container orchestration and volume handling.           |
| Cassandra startup delays | Consumers would crash on startup if the Cassandra keyspace wasn't ready.                        | Added health checks and a `cassandra-init` service to ensure `init.cql` runs and creates the keyspace if it doesn't exist. |
| Metric visibility        | Prometheus could not scrape Cassandra metrics directly, as Dropwizard metrics are not exposed.  | Installed the `jmx_prometheus_javaagent` via Dockerfile to expose JVM metrics through JMX.            |

## 🔮 Further Improvements and Future Directions

- **🧭 Reintroduce Grafana** for visual dashboards using Prometheus as a data source.
- **📍 Real-world GPS/GPRS data**: Replace simulation with actual telemetry from IoT-enabled vehicles.
- **🛡️ Security**: Introduce TLS, authentication, and role-based access to secure telemetry pipelines.
- **🌐 Geospatial Analysis**: Add mapping interfaces for route tracking, zone alerts, and geo-fencing.
- **🧠 AI/ML Integration**: Perform predictive maintenance, anomaly detection, and behavior analytics.
- **📦 Message Queue Optimization**: Introduce Kafka Streams or Flink for real-time data transformations.

## 📝 Closing Thoughts
This project demonstrates how a robust end-to-end telemetry pipeline can be built using open-This project presents a scalable, containerized architecture for real-time telemetry ingestion and monitoring. By integrating **Kafka**, **Apache Cassandra**, and **Prometheus**, it shows how high-throughput data can be reliably handled and made observable.

The removal of TimescaleDB and Grafana reflects a shift toward scalable, modular components. Cassandra provides distributed data persistence, while Prometheus enables system-level introspection with minimal overhead.

Future versions of this platform will reintegrate Grafana for visualization, add real-world telemetry inputs, and explore machine learning-based analytics to build a more intelligent and autonomous telemetry system.
