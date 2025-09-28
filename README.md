# KAMF Stack Demo - Complete Setup

## 🚀 The KAMF Stack: Building Production-Ready AI Agent Ecosystems

This demo showcases the complete KAMF Stack with all four components working together:

- **K**afka - Event streaming backbone
- **A**2A - Agent-to-Agent communication protocol
- **M**CP - Model Context Protocol for tool usage
- **F**link - Real-time stream processing

## ⚡ Quick Start (5 minutes)

```bash
# 1. Navigate to demo directory
cd */kamf-demo

# 2. Make scripts executable
chmod +x demo-scripts/*.sh

# 3. Start all services 
./demo-scripts/start-all-retry.sh

# 4. Run the unified demo 
./demo-scripts/unified-demo.sh
```

## 🎯 Unified Demos - All Components Working Together

### **Unified Interactive Demo** 
```bash
./demo-scripts/unified-demo.sh
```
- Shows complete order processing flow
- Demonstrates all 4 components interacting
- Step-by-step with explanations


### **Automated Demo with Live Data**
```bash
./demo-scripts/unified-demo-auto.sh
```
- Continuously generates orders
- Shows live metrics updating
- Good for exhibitions/booths

## 📊 What the Unified Demo Shows

The unified demo demonstrates a complete e-commerce order processing scenario:

1. **Order Creation** → Published to Kafka
2. **Agent Discovery** → Order Agent finds Inventory Agent via A2A
3. **Tool Execution** → Inventory check via MCP database tool
4. **Stream Processing** → Flink enriches order and detects fraud
5. **Customer Notification** → Email sent via MCP tool

All happening in real-time, fully integrated!

## 🏗️ Project Structure

```
kamf-demo/
├── docker-compose.yml       # Complete infrastructure
├── agents/                  # Kafka agents (Demo 1)
├── flink-jobs/             # Stream processing (Demo 2)
├── a2a-demo/               # A2A protocol (Demo 3)
├── mcp-demo/               # MCP tools (Demo 4)
└── demo-scripts/
    ├── start-all-retry.sh   # Start with retry logic
    ├── unified-demo.sh      # ⭐ MAIN UNIFIED DEMO
    ├── quick-5min-demo.sh   # Quick integrated demo
    ├── visual-demo.sh       # Dashboard-focused demo
    ├── unified-demo-auto.sh # Automated with live data
    └── monitor.sh           # Monitor all services
```

## 📺 Individual Component Demos (Optional)

If you want to show individual components:

```bash
./demo-scripts/demo-1-kafka.sh   # Kafka agents only
./demo-scripts/demo-2-flink.sh   # Flink processing only
./demo-scripts/demo-3-a2a.sh     # A2A protocol only
./demo-scripts/demo-4-mcp.sh     # MCP tools only
```

## 📍 Service URLs

- **Kafka UI**: http://localhost:8080
- **Flink Dashboard**: http://localhost:8081
- **A2A Discovery**: http://localhost:5000/a2a/discovery
- **MCP Tools**: http://localhost:6000/mcp/tools

## 🎨 Demo Highlights

### Visual Flow:
```
Customer Order → Kafka → Order Agent → A2A Discovery → 
Inventory Agent → MCP Tools → Database Query → Kafka → 
Flink Processing → Enrichment + Fraud Detection → 
Kafka → Notification Agent → MCP Email Tool → Customer
```

### Key Integration Points:
1. **Kafka ↔ Agents**: Event-driven communication
2. **Agents ↔ A2A**: Dynamic discovery
3. **Agents ↔ MCP**: Tool execution
4. **Kafka ↔ Flink**: Stream processing

## 📊 Monitoring

```bash
# Real-time monitoring
./demo-scripts/monitor.sh

# Watch specific logs
docker-compose logs -f order-agent
docker-compose logs -f flink-taskmanager
```

## 🚦 Success Metrics

Demo is successful when you show:
1. ✅ Events flowing through Kafka topics
2. ✅ Agents discovering each other via A2A
3. ✅ Tools being executed via MCP
4. ✅ Flink processing streams in real-time
5. ✅ **All working together seamlessly!**

## 💡 Key Takeaways

The unified demo proves that:
- **Integration > Individual Components**
- **Protocols + Infrastructure = Production Ready**
- **Event-driven architecture scales**
- **Standards enable ecosystem growth**

## Quick Troubleshooting

If services aren't starting:
```bash
# Check what's running
docker ps

# Restart specific service
docker-compose restart kafka

# Check logs
docker-compose logs kafka

# Full restart
./demo-scripts/stop-all.sh
./demo-scripts/start-all-retry.sh
```


## Quick Commands

```bash
# Start everything
./demo-scripts/start-all-retry.sh

# Run the main demo
./demo-scripts/unified-demo.sh

# Monitor
./demo-scripts/monitor.sh

# Stop when done
./demo-scripts/stop-all.sh
```

## 📈 Why KAMF Stack Matters

- **From 2 agents to 200+** without changing architecture
- **Handles 1000s of events/second**
- **Fault-tolerant and resilient**
- **Protocol-based, not custom integrations**
- **Production-ready from day one**

---

