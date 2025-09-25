#!/bin/bash
# Stop all KAMF Stack services

set -e

echo "🛑 Stopping KAMF Stack Demo"
echo "==========================="
echo ""

# Check if docker-compose or docker compose should be used
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

echo "Stopping all services..."
$COMPOSE_CMD down

echo ""
echo "✅ All services stopped"
echo ""
echo "To clean up volumes and data:"
echo "  $COMPOSE_CMD down -v"
