FROM cassandra:latest

ARG JMX_EXPORTER_VERSION=0.19.0
ENV JMX_EXPORTER_JAR_PATH=/opt/jmx_prometheus_javaagent.jar
ENV JMX_EXPORTER_CONFIG_PATH=/etc/cassandra/config.yml

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/app/lists/*

RUN wget -q -O ${JMX_EXPORTER_JAR_PATH} \
    "https://repo.maven.apache.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/${JMX_EXPORTER_VERSION}/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar"

COPY config.yml ${JMX_EXPORTER_CONFIG_PATH}
ENV JVM_OPTS="${JVM_OPTS} -javaagent:${JMX_EXPORTER_JAR_PATH}=8080:${JMX_EXPORTER_CONFIG_PATH} -Dcom.sun.management.jmxremote.port=7199 -Dcom.sun.management.jmxremote.rmi.port=7199 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=cassandra"
