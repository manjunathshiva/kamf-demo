#!/bin/bash
# Demo 3: A2A Protocol Demo

set -e
clear

echo "=============================================================="
echo "     DEMO 3: A2A Protocol - Agent Discovery & Communication"
echo "=============================================================="
echo ""
echo "This demo shows:"
echo "  • Agent discovery via AgentCards"
echo "  • JSON-RPC task delegation"
echo "  • Asynchronous task processing"
echo "  • Peer-to-peer agent communication"
echo ""
echo "Press Enter to continue..."
read

echo "🔍 Step 1: Discovering Agent Capabilities"
echo "-----------------------------------------"
curl -s http://localhost:5000/a2a/discovery | python3 -m json.tool

echo ""
echo "Press Enter to send a task..."
read

echo "📤 Step 2: Sending Task Request"
echo "--------------------------------"
curl -X POST http://localhost:5000/a2a/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "data_analysis",
    "params": {
      "dataset": "sales_2024",
      "metrics": ["revenue", "growth", "churn"],
      "timeframe": "Q4"
    },
    "id": "demo-task-001",
    "from_agent": "demo-client"
  }' | python3 -m json.tool

echo ""
echo "Press Enter to check task status..."
read

# Extract task ID (you might need to save it from previous command)
TASK_ID="demo-task-001"

echo "📊 Step 3: Checking Task Status"
echo "--------------------------------"
curl -s http://localhost:5000/a2a/tasks/${TASK_ID} | python3 -m json.tool

echo ""
echo "Press Enter to run Python client demo..."
read

echo "🚀 Step 4: Running Full Client Demo"
echo "------------------------------------"
docker exec -it a2a-server python agent_client.py

echo ""
echo "✅ A2A Protocol Demo Complete!"
echo ""
echo "Key Takeaways:"
echo "  • Agents discovered each other without prior knowledge"
echo "  • Tasks were delegated using standard JSON-RPC"
echo "  • Results were returned asynchronously"
echo "  • No custom integrations needed"
echo ""
