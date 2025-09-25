#!/bin/bash
# Start all KAMF Stack services with retry logic

set -e

echo "🚀 Starting KAMF Stack Demo"
echo "==========================="
echo ""

# Check if docker-compose or docker compose should be used
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# Function to retry docker pulls
retry_pull() {
    local image=$1
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Attempting to pull $image (attempt $attempt/$max_attempts)..."
        if docker pull $image; then
            echo "✅ Successfully pulled $image"
            return 0
        else
            echo "⚠️ Failed to pull $image, retrying..."
            attempt=$((attempt + 1))
            sleep 5
        fi
    done
    
    echo "❌ Failed to pull $image after $max_attempts attempts"
    return 1
}

echo "📥 Pre-pulling Docker images..."
echo "--------------------------------"

# Pull images individually with retry
retry_pull "confluentinc/cp-zookeeper:7.5.0"
retry_pull "confluentinc/cp-kafka:7.5.0"
retry_pull "provectuslabs/kafka-ui:latest"
retry_pull "flink:1.18-java11"
retry_pull "python:3.10-slim"

echo ""
echo "📊 Starting Kafka infrastructure..."
$COMPOSE_CMD up -d zookeeper

echo "⏳ Waiting for Zookeeper to be ready (20s)..."
sleep 20

echo "Starting Kafka..."
$COMPOSE_CMD up -d kafka

echo "⏳ Waiting for Kafka to be ready (30s)..."
sleep 30

echo "Starting Kafka UI..."
$COMPOSE_CMD up -d kafka-ui

echo ""
echo "🔄 Starting Flink cluster..."
$COMPOSE_CMD up -d flink-jobmanager flink-taskmanager

echo "⏳ Waiting for Flink to be ready (15s)..."
sleep 15

echo ""
echo "🤖 Building and starting Demo 1: Kafka Agents..."
$COMPOSE_CMD build order-agent inventory-agent
$COMPOSE_CMD up -d order-agent inventory-agent

echo "⏳ Waiting for agents to initialize (10s)..."
sleep 10

echo ""
echo "🌐 Building and starting Demo 3: A2A Server..."
$COMPOSE_CMD build a2a-server
$COMPOSE_CMD up -d a2a-server

echo "⏳ Waiting for A2A server (5s)..."
sleep 5

echo ""
echo "🔧 Building and starting Demo 4: MCP Server..."
$COMPOSE_CMD build mcp-server
$COMPOSE_CMD up -d mcp-server

echo "⏳ Waiting for MCP server (5s)..."
sleep 5

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📍 Service URLs:"
echo "  • Kafka UI:        http://localhost:8080"
echo "  • Flink Dashboard: http://localhost:8081"
echo "  • A2A Server:      http://localhost:5000"
echo "  • MCP Server:      http://localhost:6000"
echo ""
echo "📚 Available Demos:"
echo "  1. Kafka Agents:  ./demo-scripts/demo-1-kafka.sh"
echo "  2. Flink Stream:  ./demo-scripts/demo-2-flink.sh"
echo "  3. A2A Protocol:  ./demo-scripts/demo-3-a2a.sh"
echo "  4. MCP Tools:     ./demo-scripts/demo-4-mcp.sh"
echo ""
echo "📊 Monitor all:     ./demo-scripts/monitor.sh"
echo "🛑 Stop all:        ./demo-scripts/stop-all.sh"
