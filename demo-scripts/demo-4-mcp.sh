#!/bin/bash
# Demo 4: MCP Tool Invocation Demo

set -e
clear

echo "=============================================================="
echo "     DEMO 4: MCP - Standardized Tool Usage"
echo "=============================================================="
echo ""
echo "This demo shows:"
echo "  • Tool discovery and catalog"
echo "  • Standardized parameter validation"
echo "  • Tool execution with context"
echo "  • Execution history tracking"
echo ""
echo "Press Enter to continue..."
read

echo "🔧 Step 1: Discovering Available Tools"
echo "--------------------------------------"
curl -s http://localhost:6000/mcp/tools | python3 -m json.tool | head -50

echo ""
echo "Press Enter to execute 'query_database' tool..."
read

echo "⚡ Step 2: Executing 'query_database' Tool"
echo "------------------------------------------"
curl -X POST http://localhost:6000/mcp/tools/query_database/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "query": "SELECT * FROM orders WHERE total > 1000",
      "limit": 5
    },
    "context": {
      "user": "demo",
      "session": "demo-session"
    }
  }' | python3 -m json.tool

echo ""
echo "Press Enter to execute 'calculate_metrics' tool..."
read

echo "📊 Step 3: Executing 'calculate_metrics' Tool"
echo "---------------------------------------------"
curl -X POST http://localhost:6000/mcp/tools/calculate_metrics/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "metric_type": "revenue",
      "date_range": {
        "start": "2024-01-01",
        "end": "2024-12-31"
      }
    }
  }' | python3 -m json.tool

echo ""
echo "Press Enter to execute 'analyze_sentiment' tool..."
read

echo "💭 Step 4: Executing 'analyze_sentiment' Tool"
echo "---------------------------------------------"
curl -X POST http://localhost:6000/mcp/tools/analyze_sentiment/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "text": "The service was excellent and I am very satisfied with the product quality!",
      "language": "en"
    }
  }' | python3 -m json.tool

echo ""
echo "Press Enter to check execution history..."
read

echo "📜 Step 5: Checking Execution History"
echo "-------------------------------------"
curl -s http://localhost:6000/mcp/history?limit=5 | python3 -m json.tool

echo ""
echo "Press Enter to run full Python workflow..."
read

echo "🚀 Step 6: Running Complete Workflow"
echo "------------------------------------"
docker exec -it mcp-server python mcp_client.py

echo ""
echo "✅ MCP Demo Complete!"
echo ""
echo "Key Takeaways:"
echo "  • Tools were discovered dynamically"
echo "  • Parameters were validated automatically"
echo "  • Execution was standardized across all tools"
echo "  • No brittle custom integrations"
echo ""
