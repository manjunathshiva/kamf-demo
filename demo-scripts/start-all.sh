#!/bin/bash
# Start all KAMF Stack services

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

echo "📊 Starting Kafka infrastructure..."
$COMPOSE_CMD up -d zookeeper kafka kafka-ui

echo "⏳ Waiting for Kafka to be ready (30s)..."
sleep 30

echo ""
echo "🔄 Starting Flink cluster..."
$COMPOSE_CMD up -d flink-jobmanager flink-taskmanager

echo "⏳ Waiting for Flink to be ready (15s)..."
sleep 15

echo ""
echo "🤖 Starting Demo 1: Kafka Agents..."
$COMPOSE_CMD up -d order-agent inventory-agent

echo "⏳ Waiting for agents to initialize (10s)..."
sleep 10

echo ""
echo "🌐 Starting Demo 3: A2A Server..."
$COMPOSE_CMD up -d a2a-server

echo "⏳ Waiting for A2A server (5s)..."
sleep 5

echo ""
echo "🔧 Starting Demo 4: MCP Server..."
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
