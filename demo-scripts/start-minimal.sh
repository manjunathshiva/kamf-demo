#!/bin/bash
# Quick start with minimal services for testing

set -e

echo "🚀 Quick Start - Minimal Services"
echo "================================="
echo ""

# Check if docker-compose or docker compose should be used
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

echo "🔍 Checking Docker daemon..."
if ! docker ps &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is running"
echo ""

echo "🧹 Cleaning up any existing containers..."
$COMPOSE_CMD down 2>/dev/null || true

echo ""
echo "📥 Pulling essential images (this may take a few minutes)..."
echo ""

# Try alternative Kafka images if Confluent fails
echo "Option 1: Trying Bitnami Kafka (alternative)..."
docker pull bitnami/zookeeper:latest || true
docker pull bitnami/kafka:latest || true

echo ""
echo "Starting with available images..."
echo ""

# Create alternative docker-compose for Bitnami
cat > docker-compose-lite.yml << 'EOF'
version: '3.8'

services:
  zookeeper:
    image: bitnami/zookeeper:latest
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes
    networks:
      - kamf-network

  kafka:
    image: bitnami/kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:29092,PLAINTEXT_HOST://:9092
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
    depends_on:
      - zookeeper
    networks:
      - kamf-network

  a2a-server:
    build:
      context: ./a2a-demo
      dockerfile: Dockerfile
    container_name: a2a-server
    ports:
      - "5000:5000"
    environment:
      A2A_PORT: 5000
      PYTHONUNBUFFERED: 1
    volumes:
      - ./a2a-demo:/app
    command: python agent_server.py
    networks:
      - kamf-network

  mcp-server:
    build:
      context: ./mcp-demo
      dockerfile: Dockerfile
    container_name: mcp-server
    ports:
      - "6000:6000"
    environment:
      MCP_PORT: 6000
      PYTHONUNBUFFERED: 1
    volumes:
      - ./mcp-demo:/app
    command: python mcp_server.py
    networks:
      - kamf-network

networks:
  kamf-network:
    driver: bridge
EOF

echo "Using lightweight Kafka setup..."
$COMPOSE_CMD -f docker-compose-lite.yml up -d zookeeper kafka

echo "⏳ Waiting for Kafka to start (30s)..."
sleep 30

echo ""
echo "🌐 Starting A2A and MCP servers..."
$COMPOSE_CMD -f docker-compose-lite.yml build a2a-server mcp-server
$COMPOSE_CMD -f docker-compose-lite.yml up -d a2a-server mcp-server

echo ""
echo "✅ Core services started!"
echo ""
echo "📍 Available Services:"
echo "  • Kafka:      localhost:9092"
echo "  • A2A Server: http://localhost:5000"
echo "  • MCP Server: http://localhost:6000"
echo ""
echo "🧪 Test commands:"
echo "  curl http://localhost:5000/a2a/discovery"
echo "  curl http://localhost:6000/mcp/tools"
echo ""
echo "📝 Note: Using Bitnami Kafka instead of Confluent due to download issues"
