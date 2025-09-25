# KAMF Demo - A2A and MCP Protocols

## Quick Start Guide

### Prerequisites

1. **Python 3.10+** installed
2. **Docker** (optional, for containerized demo)
3. **Required Python packages**:
   ```bash
   pip install aiohttp
   ```

### Project Structure
```
kamf-demo/
├── a2a-demo/           # Demo 3: A2A Protocol
│   ├── agent_server.py # A2A server implementation
│   ├── agent_client.py # A2A client for testing
│   ├── requirements.txt
│   └── Dockerfile
├── mcp-demo/           # Demo 4: MCP Protocol
│   ├── mcp_server.py   # MCP server with tools
│   ├── mcp_client.py   # MCP client for testing
│   ├── requirements.txt
│   └── Dockerfile
└── demo-scripts/       # Demo execution scripts
    ├── demo-3-a2a.sh   # A2A demo with Docker
    ├── demo-4-mcp.sh   # MCP demo with Docker
    ├── test-a2a-local.sh # Local A2A test
    └── test-mcp-local.sh # Local MCP test
```

## Running Demo 3: A2A Protocol

### Option 1: Run Locally (Quick Test)

```bash
# Install dependencies
pip install aiohttp

# Make scripts executable
chmod +x demo-scripts/*.sh

# Run local test
./demo-scripts/test-a2a-local.sh
```

### Option 2: Run with Docker

```bash
# Build and start containers
docker-compose up -d a2a-server

# Run the demo script
./demo-scripts/demo-3-a2a.sh
```

### Option 3: Manual Testing

```bash
# Terminal 1: Start server
cd a2a-demo
python3 agent_server.py

# Terminal 2: Test with curl
# Discovery
curl http://localhost:5000/a2a/discovery | python3 -m json.tool

# Send task
curl -X POST http://localhost:5000/a2a/tasks \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"data_analysis","params":{"dataset":"sales_2024"},"id":"test-1"}' \
  | python3 -m json.tool

# Terminal 3: Run client
cd a2a-demo
python3 agent_client.py
```

## Running Demo 4: MCP Protocol

### Option 1: Run Locally (Quick Test)

```bash
# Install dependencies
pip install aiohttp

# Run local test
./demo-scripts/test-mcp-local.sh
```

### Option 2: Run with Docker

```bash
# Build and start containers
docker-compose up -d mcp-server

# Run the demo script
./demo-scripts/demo-4-mcp.sh
```

### Option 3: Manual Testing

```bash
# Terminal 1: Start server
cd mcp-demo
python3 mcp_server.py

# Terminal 2: Test with curl
# List tools
curl http://localhost:6000/mcp/tools | python3 -m json.tool

# Execute a tool
curl -X POST http://localhost:6000/mcp/tools/get_weather/execute \
  -H "Content-Type: application/json" \
  -d '{"parameters":{"location":"San Francisco","units":"celsius"}}' \
  | python3 -m json.tool

# Terminal 3: Run client
cd mcp-demo
python3 mcp_client.py        # Full workflow
python3 mcp_client.py simple # Simple demo
```

## Demo Highlights for Presentation

### A2A Protocol (Demo 3)

**Key Points to Show:**
1. **Discovery**: Agents announce their capabilities
2. **Task Delegation**: Standard JSON-RPC format
3. **Async Processing**: Non-blocking task execution
4. **Results**: Structured response with artifacts

**Visual Output:**
- Clear ASCII art separators mark each phase
- Color-coded output (if terminal supports)
- Real-time task status updates

### MCP Protocol (Demo 4)

**Key Points to Show:**
1. **Tool Catalog**: Dynamic tool discovery
2. **Parameter Validation**: Automatic checking
3. **Execution**: Standardized across all tools
4. **History**: Complete audit trail

**Visual Output:**
- Tool categories and descriptions
- Execution timing metrics
- Result previews

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :5000  # For A2A
lsof -i :6000  # For MCP

# Kill the process
kill -9 <PID>
```

### Module Not Found
```bash
# Install dependencies
pip install aiohttp
```

### Permission Denied
```bash
# Make scripts executable
chmod +x demo-scripts/*.sh
chmod +x setup-permissions.sh
./setup-permissions.sh
```

## Presentation Tips

1. **Start servers early**: Launch before demo starts
2. **Test connectivity**: Verify ports are accessible
3. **Use split terminal**: Show server logs + client
4. **Highlight visual output**: Point out the === separators
5. **Explain each phase**: Pause at visual markers

## Demo Timing

- **A2A Demo**: 3 minutes
  - Discovery: 30 seconds
  - Task submission: 45 seconds
  - Status check: 30 seconds
  - Full workflow: 1 minute
  - Explanation: 45 seconds

- **MCP Demo**: 3 minutes
  - Tool discovery: 30 seconds
  - Execute 3 tools: 90 seconds
  - Show history: 30 seconds
  - Full workflow: 1 minute
  - Explanation: 30 seconds

## Key Takeaways

### A2A Protocol
- No hardcoded integrations
- Agents discover each other dynamically
- Standard communication format
- Asynchronous, non-blocking

### MCP Protocol
- Tools as first-class citizens
- Automatic parameter validation
- Consistent execution model
- Complete observability

## Additional Resources

- A2A Specification: https://github.com/google/a2a
- MCP Documentation: https://modelcontextprotocol.io
- Presentation Slides: [Add your link]
- Full KAMF Stack Demo: [Parent directory]

## Support

If you encounter issues during the presentation:
1. Have backup screenshots ready
2. Use the local test scripts (faster than Docker)
3. Show the code structure if demo fails
4. Emphasize this is why production infrastructure matters

Good luck with your presentation! 🚀
