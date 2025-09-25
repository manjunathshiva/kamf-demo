#!/bin/bash
# Demo 2: Flink Real-time Processing

set -e
clear

echo "=============================================================="
echo "     DEMO 2: Real-time Event Processing with Flink"
echo "=============================================================="
echo ""
echo "This demo shows:"
echo "  • Flink consuming Kafka streams"
echo "  • Real-time order enrichment"
echo "  • Fraud detection patterns"
echo "  • Window aggregations every 30 seconds"
echo ""
echo "Press Enter to continue..."
read

echo "📊 Opening Flink Dashboard..."
echo "   URL: http://localhost:8081"
echo ""

# Try to open browser (works on Mac)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8081 2>/dev/null || echo "Please open http://localhost:8081 manually"
else
    echo "Please open http://localhost:8081 in your browser"
fi

echo ""
echo "Press Enter to submit Flink job..."
read

echo "🚀 Submitting Flink Job..."
echo "============================"

# Submit the Flink job
docker exec flink-jobmanager /opt/flink/bin/flink run -py /opt/flink/jobs/order_processor.py 2>/dev/null || {
    echo "Note: Job might already be running. Check the Flink dashboard."
}

echo ""
echo "✅ Job submitted! Check the Flink dashboard for:"
echo "  • Running jobs graph"
echo "  • Task metrics"
echo "  • Checkpoints"
echo "  • Throughput metrics"
echo ""
echo "Press Enter to see enriched orders in Kafka..."
read

echo "📦 Checking Enriched Orders Topic:"
docker exec kafka kafka-console-consumer \
    --bootstrap-server localhost:29092 \
    --topic enriched-orders \
    --from-beginning \
    --max-messages 3 \
    --timeout-ms 5000 2>/dev/null || echo "No enriched orders yet. Wait a moment and try again."

echo ""
echo "Press Enter to see aggregated statistics..."
read

echo "📈 Checking Order Statistics Topic:"
docker exec kafka kafka-console-consumer \
    --bootstrap-server localhost:29092 \
    --topic order-statistics \
    --from-beginning \
    --max-messages 2 \
    --timeout-ms 5000 2>/dev/null || echo "Statistics will appear after 30-second window. Please wait."

echo ""
echo "Press Enter to see Flink job logs..."
read

echo "📜 Flink Task Manager Logs (last 50 lines):"
docker logs --tail 50 flink-taskmanager

echo ""
echo "✅ Demo 2 Complete!"
echo ""
echo "Key Takeaways:"
echo "  • Real-time stream processing at scale"
echo "  • Complex event processing (fraud detection)"
echo "  • Stateful computations with checkpointing"
echo "  • Window-based aggregations"
echo "  • Fault-tolerant processing"
