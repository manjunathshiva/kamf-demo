#!/bin/bash
# Test demos without Kafka/Docker - just Python servers

echo "🚀 Running Demos Locally (No Docker Required)"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip3 install aiohttp kafka-python --quiet

echo ""
echo "Choose a demo to run locally:"
echo "1) A2A Protocol Demo"
echo "2) MCP Tools Demo"
echo "3) Both demos"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting A2A Demo..."
        cd a2a-demo
        # Start server in background
        python3 agent_server.py &
        SERVER_PID=$!
        echo "A2A Server started (PID: $SERVER_PID)"
        echo "Server URL: http://localhost:5000"
        sleep 3
        
        echo ""
        echo "Running client demo..."
        python3 agent_client.py
        
        echo ""
        echo "Stopping server..."
        kill $SERVER_PID 2>/dev/null
        ;;
        
    2)
        echo "Starting MCP Demo..."
        cd mcp-demo
        # Start server in background
        python3 mcp_server.py &
        SERVER_PID=$!
        echo "MCP Server started (PID: $SERVER_PID)"
        echo "Server URL: http://localhost:6000"
        sleep 3
        
        echo ""
        echo "Running client demo..."
        python3 mcp_client.py simple
        
        echo ""
        echo "Stopping server..."
        kill $SERVER_PID 2>/dev/null
        ;;
        
    3)
        echo "Starting both demos..."
        
        # Start A2A
        cd a2a-demo
        python3 agent_server.py &
        A2A_PID=$!
        cd ..
        
        # Start MCP
        cd mcp-demo
        python3 mcp_server.py &
        MCP_PID=$!
        cd ..
        
        echo "Servers started:"
        echo "  A2A: http://localhost:5000 (PID: $A2A_PID)"
        echo "  MCP: http://localhost:6000 (PID: $MCP_PID)"
        
        sleep 3
        
        echo ""
        echo "Running A2A client..."
        cd a2a-demo && python3 agent_client.py
        cd ..
        
        echo ""
        echo "Running MCP client..."
        cd mcp-demo && python3 mcp_client.py simple
        cd ..
        
        echo ""
        echo "Stopping servers..."
        kill $A2A_PID $MCP_PID 2>/dev/null
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Demo complete!"
