# ============================================

# flink-jobs/Dockerfile
FROM flink:1.18-java11

# Install Python and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install apache-flink kafka-python

WORKDIR /opt/flink/jobs

COPY . .