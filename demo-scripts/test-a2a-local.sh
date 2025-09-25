#!/bin/bash
# Test A2A locally without Docker

echo "Starting A2A Server locally..."
echo "Make sure you have installed: pip install aiohttp"
echo ""

# Start server in background
cd a2a-demo
python3 agent_server.py &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
sleep 3

echo ""
echo "Running client demo..."
python3 agent_client.py

echo ""
echo "Stopping server..."
kill $SERVER_PID

echo "Test complete!"
