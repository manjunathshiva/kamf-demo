#!/bin/bash
# Demo 1: Kafka Agents Communication

set -e
clear

echo "=============================================================="
echo "     DEMO 1: Two Agents Communicating via Kafka"
echo "=============================================================="
echo ""
echo "This demo shows:"
echo "  • Order Agent publishing events to Kafka"
echo "  • Inventory Agent consuming and responding"
echo "  • Event-driven architecture in action"
echo "  • Decoupled communication at scale"
echo ""
echo "Press Enter to continue..."
read

echo "📊 Opening Kafka UI in browser..."
echo "   URL: http://localhost:8080"
echo ""

# Try to open browser (works on Mac)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8080 2>/dev/null || echo "Please open http://localhost:8080 manually"
else
    echo "Please open http://localhost:8080 in your browser"
fi

echo ""
echo "Press Enter to see Kafka topics..."
read

echo "📋 Kafka Topics:"
docker exec kafka kafka-topics --list --bootstrap-server localhost:29092

echo ""
echo "Press Enter to watch agent communication..."
read

echo "👀 Watching Agent Logs (Press Ctrl+C to stop):"
echo "============================================"
echo ""
echo "You will see:"
echo "  • Orders being created every 15 seconds"
echo "  • Inventory checks happening in real-time"
echo "  • Responses flowing back through Kafka"
echo ""

# Show logs from both agents
docker-compose logs -f --tail=50 order-agent inventory-agent

echo ""
echo "✅ Demo 1 Complete!"
echo ""
echo "Key Takeaways:"
echo "  • Agents communicate without knowing each other"
echo "  • Kafka provides reliable message delivery"
echo "  • System scales to hundreds of agents"
echo "  • Full decoupling and fault tolerance"
