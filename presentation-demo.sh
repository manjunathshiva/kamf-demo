#!/bin/bash
# PRESENTATION DEMO - Works without Docker!

clear
echo "=================================================="
echo "    KAMF STACK DEMO - PRESENTATION MODE"
echo "    (No Docker Required - Pure Python)"
echo "=================================================="
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install aiohttp kafka-python --quiet 2>/dev/null || {
    echo "Installing with pip..."
    pip install aiohttp kafka-python --quiet 2>/dev/null
}

echo "✅ Dependencies ready"
echo ""

function run_a2a_demo() {
    echo "============================================"
    echo "    DEMO 3: A2A Protocol"
    echo "============================================"
    echo ""
    
    cd a2a-demo
    
    # Start server
    echo "🚀 Starting A2A Server..."
    python3 agent_server.py &
    SERVER_PID=$!
    sleep 2
    
    echo ""
    echo "📍 A2A Server running at http://localhost:5000"
    echo ""
    echo "Press Enter to discover agent..."
    read
    
    # Discovery
    echo "🔍 Agent Discovery:"
    curl -s http://localhost:5000/a2a/discovery | python3 -m json.tool | head -20
    
    echo ""
    echo "Press Enter to send task..."
    read
    
    # Send task
    echo "📤 Sending Task:"
    curl -X POST http://localhost:5000/a2a/tasks \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"data_analysis","params":{"dataset":"sales_2024"},"id":"demo-1"}' \
        | python3 -m json.tool
    
    echo ""
    echo "Press Enter to run full client demo..."
    read
    
    # Run client
    python3 agent_client.py
    
    # Cleanup
    kill $SERVER_PID 2>/dev/null
    cd ..
    
    echo ""
    echo "✅ A2A Demo Complete!"
    echo ""
}

function run_mcp_demo() {
    echo "============================================"
    echo "    DEMO 4: MCP Tool Usage"
    echo "============================================"
    echo ""
    
    cd mcp-demo
    
    # Start server
    echo "🚀 Starting MCP Server..."
    python3 mcp_server.py &
    SERVER_PID=$!
    sleep 2
    
    echo ""
    echo "📍 MCP Server running at http://localhost:6000"
    echo ""
    echo "Press Enter to discover tools..."
    read
    
    # List tools
    echo "🔧 Available Tools:"
    curl -s http://localhost:6000/mcp/tools | python3 -m json.tool | head -30
    
    echo ""
    echo "Press Enter to execute a tool..."
    read
    
    # Execute tool
    echo "⚡ Executing Weather Tool:"
    curl -X POST http://localhost:6000/mcp/tools/get_weather/execute \
        -H "Content-Type: application/json" \
        -d '{"parameters":{"location":"San Francisco","units":"celsius"}}' \
        | python3 -m json.tool
    
    echo ""
    echo "Press Enter to run full workflow..."
    read
    
    # Run client
    python3 mcp_client.py simple
    
    # Cleanup
    kill $SERVER_PID 2>/dev/null
    cd ..
    
    echo ""
    echo "✅ MCP Demo Complete!"
    echo ""
}

# Main menu
echo "Select demo to run:"
echo "1) A2A Protocol (Demo 3)"
echo "2) MCP Tools (Demo 4)"
echo "3) Both Demos (Sequential)"
echo "4) Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        run_a2a_demo
        ;;
    2)
        run_mcp_demo
        ;;
    3)
        run_a2a_demo
        echo "Press Enter to continue to MCP demo..."
        read
        run_mcp_demo
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "    PRESENTATION DEMO COMPLETE!"
echo "=================================================="
echo ""
echo "Key Takeaways Shown:"
echo "✅ Agent discovery without hardcoding"
echo "✅ Standardized tool execution"
echo "✅ Protocol-based communication"
echo "✅ No brittle integrations needed"
echo ""
