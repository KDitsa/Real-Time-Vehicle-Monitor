FROM flink:1.19-scala_2.12-java17

RUN wget -P /opt/flink/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.2.0-1.19/flink-sql-connector-kafka-3.2.0-1.19.jar; \
    wget -P /opt/flink/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar; \
    wget -P /opt/flink/lib https://repo.maven.apache.org/maven2/org/apache/flink/flink-python/1.19.3/flink-python-1.19.3.jar; \
    wget -P /opt/flink/lib https://repo.maven.apache.org/maven2/org/postgresql/postgresql/42.7.7/postgresql-42.7.7.jar;

RUN apt-get update -y && \
apt-get install -y python3 python3-pip python3-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /opt/flink
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY flink.py .
COPY config.py .
