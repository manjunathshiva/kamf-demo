#!/bin/bash
# Setup script to make everything ready

echo "🚀 KAMF Demo Setup"
echo "=================="
echo ""

# Make all scripts executable
echo "Setting permissions..."
chmod +x demo-scripts/*.sh
chmod +x flink-jobs/submit_job.sh

echo "✅ All scripts are now executable"
echo ""

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    docker --version
else
    echo "❌ Docker is not installed. Please install Docker Desktop."
    exit 1
fi

echo ""
echo "Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose is available"
    docker-compose --version
elif docker compose version &> /dev/null; then
    echo "✅ docker compose is available"
    docker compose version
else
    echo "❌ Docker Compose is not available"
    exit 1
fi

echo ""
echo "📁 Project Structure:"
echo "--------------------"
ls -la

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Start all services:  ./demo-scripts/start-all.sh"
echo "2. Run individual demos:"
echo "   - Demo 1 (Kafka):    ./demo-scripts/demo-1-kafka.sh"
echo "   - Demo 2 (Flink):    ./demo-scripts/demo-2-flink.sh"
echo "   - Demo 3 (A2A):      ./demo-scripts/demo-3-a2a.sh"
echo "   - Demo 4 (MCP):      ./demo-scripts/demo-4-mcp.sh"
echo "3. Monitor services:    ./demo-scripts/monitor.sh"
echo "4. Stop all:           ./demo-scripts/stop-all.sh"
echo ""
echo "Good luck with your presentation! 🎉"
