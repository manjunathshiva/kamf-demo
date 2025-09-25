# KAMF Stack Demo - Complete Setup

## 🚀 The KAMF Stack: Building Production-Ready AI Agent Ecosystems

This demo showcases the complete KAMF Stack with all four components working together:

- **K**afka - Event streaming backbone
- **A**2A - Agent-to-Agent communication protocol
- **M**CP - Model Context Protocol for tool usage
- **F**link - Real-time stream processing

## 📋 Prerequisites

- **Docker Desktop** installed and running
- **Python 3.10+** (for local testing)
- **8-10GB RAM** available
- **Ports available**: 2181, 5000-5002, 6000, 8080, 8081, 9092

## 🏗️ Project Structure

```
kamf-demo/
├── docker-compose.yml      # Complete infrastructure setup
├── agents/                 # Demo 1: Kafka Agents
│   ├── order_agent.py      # Order processing agent
│   ├── inventory_agent.py  # Inventory checking agent
│   ├── requirements.txt
│   └── Dockerfile
├── flink-jobs/            # Demo 2: Flink Processing
│   ├── order_processor.py # Stream processing job
│   ├── submit_job.sh      # Job submission script
│   ├── requirements.txt
│   └── Dockerfile
├── a2a-demo/              # Demo 3: A2A Protocol
│   ├── agent_server.py    # A2A server implementation
│   ├── agent_client.py    # A2A client for testing
│   ├── requirements.txt
│   └── Dockerfile
├── mcp-demo/              # Demo 4: MCP Protocol
│   ├── mcp_server.py      # MCP server with tools
│   ├── mcp_client.py      # MCP client for testing
│   ├── requirements.txt
│   └── Dockerfile
└── demo-scripts/          # Demo execution scripts
    ├── start-all.sh       # Start all services
    ├── stop-all.sh        # Stop all services
    ├── monitor.sh         # Monitor all services
    ├── demo-1-kafka.sh    # Kafka agents demo
    ├── demo-2-flink.sh    # Flink processing demo
    ├── demo-3-a2a.sh      # A2A protocol demo
    └── demo-4-mcp.sh      # MCP tools demo
```

## ⚡ Quick Start (5 minutes)

```bash
# 1. Clone/navigate to the demo directory
cd /Users/manjunm4/meetup/agentnexas/kamf-demo

# 2. Make all scripts executable
chmod +x demo-scripts/*.sh

# 3. Start all services
./demo-scripts/start-all-retry.sh  

# 4. Wait for services to be ready (about 1 minute)

# 5. Run demos individually
./demo-scripts/demo-1-kafka.sh   # Demo 1: Kafka Agents
./demo-scripts/demo-2-flink.sh   # Demo 2: Flink Processing
./demo-scripts/demo-3-a2a.sh     # Demo 3: A2A Protocol
./demo-scripts/demo-4-mcp.sh     # Demo 4: MCP Tools

# 6. Monitor all services
./demo-scripts/monitor.sh

# 7. Stop everything when done
./demo-scripts/stop-all.sh
```

## 📺 Individual Demos

### Demo 1: Kafka - Agent Communication (3 minutes)

**What it shows:**
- Order agent creating orders every 15 seconds
- Inventory agent checking stock in real-time
- Event-driven communication through Kafka
- Decoupled, scalable architecture

**Run:**
```bash
./demo-scripts/demo-1-kafka.sh
```

**Key Points:**
- Agents don't know about each other
- Kafka handles routing and durability
- System scales to hundreds of agents

**Visual Elements:**
- Kafka UI: http://localhost:8080
- Real-time log streaming
- Order creation and inventory checks

### Demo 2: Flink - Real-time Processing (3 minutes)

**What it shows:**
- Stream processing of order events
- Real-time fraud detection
- Window-based aggregations (30 seconds)
- Stateful processing with checkpointing

**Run:**
```bash
./demo-scripts/demo-2-flink.sh
```

**Key Points:**
- Processes thousands of events/second
- Complex event correlation
- Fault-tolerant with exactly-once semantics

**Visual Elements:**
- Flink Dashboard: http://localhost:8081
- Job graph visualization
- Metrics and throughput

### Demo 3: A2A Protocol - Agent Discovery (3 minutes)

**What it shows:**
- Agent capability discovery via AgentCards
- JSON-RPC task delegation
- Asynchronous task processing
- Standardized communication

**Run:**
```bash
./demo-scripts/demo-3-a2a.sh
```

**Key Points:**
- No hardcoded integrations
- Agents discover each other dynamically
- Protocol-based communication

**Visual Elements:**
- JSON AgentCard responses
- Task submission and monitoring
- Real-time status updates

### Demo 4: MCP - Tool Usage (3 minutes)

**What it shows:**
- Dynamic tool discovery
- Parameter validation
- Standardized tool execution
- Execution history tracking

**Run:**
```bash
./demo-scripts/demo-4-mcp.sh
```

**Key Points:**
- Tools as first-class citizens
- Automatic parameter validation
- Plug-and-play architecture

**Visual Elements:**
- Tool catalog with 5 different tools
- Execution metrics
- Workflow orchestration

## 🎯 Presentation Flow (30 minutes)

### Suggested Timeline:
1. **Introduction** (2 min) - Problem statement
2. **KAMF Overview** (3 min) - Stack components
3. **Demo 1: Kafka** (5 min) - Event streaming
4. **Demo 2: Flink** (5 min) - Stream processing
5. **Demo 3: A2A** (5 min) - Agent communication
6. **Demo 4: MCP** (5 min) - Tool standardization
7. **Integration** (3 min) - How they work together
8. **Q&A** (2 min)

### Pro Tips:
- Start all services 5 minutes before presentation
- Have browser tabs open: Kafka UI, Flink Dashboard
- Use split terminal: logs on left, commands on right
- Keep `monitor.sh` running in a visible window

## 📊 Monitoring & Debugging

### Monitor All Services:
```bash
# Real-time monitoring
watch -n 2 ./demo-scripts/monitor.sh

# Check specific service logs
docker-compose logs -f order-agent
docker-compose logs -f flink-jobmanager
docker-compose logs -f a2a-server
docker-compose logs -f mcp-server
```

### Service URLs:
- **Kafka UI**: http://localhost:8080
- **Flink Dashboard**: http://localhost:8081
- **A2A Discovery**: http://localhost:5000/a2a/discovery
- **MCP Tools**: http://localhost:6000/mcp/tools

### Common Issues:

**Port already in use:**
```bash
# Find process using port
lsof -i :8080
# Kill process
kill -9 <PID>
```

**Kafka not starting:**
```bash
# Clean up and restart
docker-compose down -v
docker-compose up -d kafka zookeeper
```

**Flink job not running:**
```bash
# Submit job manually
docker exec flink-jobmanager /opt/flink/bin/flink run -py /opt/flink/jobs/order_processor.py
```

## 🧪 Local Testing (without Docker)

For quick tests without Docker:

```bash
# Install Python dependencies
pip install aiohttp kafka-python

# Test A2A locally
cd a2a-demo
python3 agent_server.py &
python3 agent_client.py

# Test MCP locally
cd mcp-demo
python3 mcp_server.py &
python3 mcp_client.py
```

## 🎨 Demo Highlights

### Visual Indicators:
- 🔍 Discovery
- 📋 Task/Tool execution
- ✅ Success
- ❌ Failure
- ⏳ Processing
- 📊 Metrics

### Console Formatting:
- Clear section separators (`====`)
- Colored output (if terminal supports)
- Progress indicators
- Real-time updates

## 🚦 Success Metrics

Your demo is successful when you show:
1. ✅ Agents communicating via Kafka without direct connections
2. ✅ Flink processing streams in real-time with fraud detection
3. ✅ A2A agents discovering and delegating tasks
4. ✅ MCP tools being executed with validation

## 🛠️ Cleanup

```bash
# Stop all services
./demo-scripts/stop-all.sh

# Remove all data and volumes
docker-compose down -v

# Remove all containers and images
docker system prune -af
```

## 📚 Resources

- **Apache Kafka**: https://kafka.apache.org
- **Apache Flink**: https://flink.apache.org
- **A2A Protocol**: https://github.com/google/a2a
- **MCP Protocol**: https://modelcontextprotocol.io
- **12-Factor Agents**: https://github.com/humanlayer/12-factor-agents

## 💡 Key Takeaways

1. **Protocols aren't enough** - You need infrastructure
2. **Event-driven > Point-to-point** - For scale and resilience
3. **Standards enable ecosystems** - Like HTTP enabled the web
4. **Production-ready matters** - Not just demos, but real systems

## 🆘 Troubleshooting During Presentation

If something fails during the demo:
1. **Stay calm** - "This is exactly why we need production-grade infrastructure"
2. **Use monitor script** - Show what's still running
3. **Have backup** - Screenshots or pre-recorded video
4. **Explain the value** - Focus on concepts if demo fails

## ✨ Final Notes

This demo showcases a complete, production-ready AI agent ecosystem. Each component is essential:
- **Kafka** provides the nervous system
- **Flink** provides the real-time brain
- **A2A** provides the common language
- **MCP** provides the tool standardization

Together, they form the foundation for building scalable, resilient, and intelligent agent systems that can grow from 2 agents to 200+ without changing the architecture.

## 🎬 Demo Commands Cheatsheet

```bash
# Quick commands for presentation
curl -s http://localhost:5000/a2a/discovery | jq .          # A2A discovery
curl -s http://localhost:6000/mcp/tools | jq '.tools[0]'    # MCP tools
docker exec kafka kafka-topics --list --bootstrap-server localhost:29092
docker logs --tail 10 order-agent                           # Recent logs
```

## 📈 Metrics to Highlight

During your presentation, emphasize:
- **Kafka**: 1000s of messages/sec capability
- **Flink**: Sub-second processing latency
- **A2A**: Zero-config agent discovery
- **MCP**: 5 tool categories, unlimited tools

Good luck with your presentation! 🚀

---
*Built with ❤️ for the AI Agent community*
