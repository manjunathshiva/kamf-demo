#!/bin/bash
# Test MCP locally without Docker

echo "Starting MCP Server locally..."
echo "Make sure you have installed: pip install aiohttp"
echo ""

# Start server in background
cd mcp-demo
python3 mcp_server.py &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
sleep 3

echo ""
echo "Running client demo..."
python3 mcp_client.py

echo ""
echo "Running simple demo..."
python3 mcp_client.py simple

echo ""
echo "Stopping server..."
kill $SERVER_PID

echo "Test complete!"
