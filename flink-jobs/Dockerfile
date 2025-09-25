# ============================================

# flink-jobs/Dockerfile
FROM flink:1.18-java11

# Set JAVA_HOME for proper JDK detection
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

# Install Python, JDK development headers, and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip openjdk-11-jdk-headless build-essential wget && \
    pip3 install apache-flink==1.18.0 kafka-python protobuf grpcio && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download Kafka connector JAR (using working URL)
RUN wget -O /opt/flink/lib/flink-sql-connector-kafka-1.17.1.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.1/flink-sql-connector-kafka-1.17.1.jar

WORKDIR /opt/flink/jobs

COPY . .