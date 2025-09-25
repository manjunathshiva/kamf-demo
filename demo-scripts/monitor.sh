#!/bin/bash
# Monitor all KAMF Stack services

clear
echo "📊 KAMF Stack Monitor"
echo "====================="
echo ""

# Function to check service health
check_service() {
    local service=$1
    local url=$2
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null | grep -q "200\|302"; then
        echo "✅ $service: Running"
    else
        echo "❌ $service: Not responding"
    fi
}

echo "🔍 Checking Services..."
echo "-----------------------"
check_service "Kafka UI" "http://localhost:8080"
check_service "Flink Dashboard" "http://localhost:8081"
check_service "A2A Server" "http://localhost:5000/a2a/discovery"
check_service "MCP Server" "http://localhost:6000/mcp/health"

echo ""
echo "🐳 Docker Container Status:"
echo "---------------------------"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(NAME|kafka|flink|agent|a2a|mcp)" || echo "No KAMF containers running"

echo ""
echo "📨 Kafka Topics:"
echo "----------------"
docker exec kafka kafka-topics --list --bootstrap-server localhost:29092 2>/dev/null || echo "Kafka not ready"

echo ""
echo "📊 Message Counts:"
echo "------------------"
for topic in order-events inventory-responses enriched-orders order-statistics; do
    count=$(docker exec kafka kafka-run-class kafka.tools.GetOffsetShell \
        --broker-list localhost:29092 \
        --topic $topic 2>/dev/null | awk -F':' '{sum += $3} END {print sum}')
    
    if [ -n "$count" ]; then
        echo "  $topic: $count messages"
    fi
done 2>/dev/null || echo "  Unable to fetch message counts"

echo ""
echo "🔄 Auto-refresh: watch -n 2 ./demo-scripts/monitor.sh"
echo "📜 View logs:    docker-compose logs -f [service-name]"
echo "🛑 Stop all:     ./demo-scripts/stop-all.sh"
