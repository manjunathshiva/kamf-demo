"""
MCP Client - Demonstrates tool discovery and execution
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MCP-Client')

class MCPClient:
    """Client for interacting with MCP server"""
    
    def __init__(self, server_url: str = "http://localhost:6000"):
        self.server_url = server_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
    
    async def discover_tools(self):
        """Discover available tools"""
        async with self.session.get(f"{self.server_url}/mcp/tools") as resp:
            data = await resp.json()
            
            print("\n" + "="*60)
            print("🔧 DISCOVERED MCP TOOLS")
            print(f"   Total: {data['count']} tools")
            print(f"   Categories: {', '.join(data['categories'])}")
            print("\n   Available Tools:")
            for tool in data['tools']:
                print(f"      📌 {tool['name']}")
                print(f"         {tool['description']}")
                print(f"         Category: {tool['category']}")
                print(f"         Required: {tool['parameters'].get('required', [])}")
            print("="*60 + "\n")
            
            return data['tools']
    
    async def execute_tool(self, tool_name: str, parameters: dict, context: dict = None):
        """Execute a tool"""
        payload = {
            'parameters': parameters,
            'context': context or {}
        }
        
        print(f"\n🎯 Executing tool: {tool_name}")
        print(f"   Parameters: {json.dumps(parameters, indent=2)}")
        
        async with self.session.post(
            f"{self.server_url}/mcp/tools/{tool_name}/execute",
            json=payload
        ) as resp:
            result = await resp.json()
            
            if result.get('success'):
                print(f"   ✅ Success! Execution time: {result.get('execution_time_ms')}ms")
                print(f"   Result Preview:")
                result_str = json.dumps(result.get('result'), indent=2)
                # Truncate if too long
                if len(result_str) > 500:
                    result_str = result_str[:500] + "..."
                print(f"{result_str}")
            else:
                print(f"   ❌ Failed: {result.get('error')}")
            
            return result
    
    async def get_health(self):
        """Check server health"""
        async with self.session.get(f"{self.server_url}/mcp/health") as resp:
            return await resp.json()
    
    async def get_history(self, limit: int = 5):
        """Get execution history"""
        async with self.session.get(f"{self.server_url}/mcp/history?limit={limit}") as resp:
            return await resp.json()

async def demo_workflow():
    """Run a complete MCP demo workflow"""
    print("\n" + "="*70)
    print(" "*20 + "MCP DEMO WORKFLOW")
    print(" "*10 + "Order Analysis & Customer Notification")
    print("="*70)
    
    async with MCPClient() as client:
        # Check health
        print("\n📍 Checking MCP Server Health...")
        health = await client.get_health()
        print(f"   Status: {health['status']}")
        print(f"   Tools: {health['tools_available']}")
        
        await asyncio.sleep(1)
        
        # Step 1: Discover tools
        print("\n📍 PHASE 1: Tool Discovery")
        print("-" * 40)
        tools = await client.discover_tools()
        
        await asyncio.sleep(2)
        
        # Step 2: Query database
        print("\n📍 PHASE 2: Database Query")
        print("-" * 40)
        print("Querying high-value orders...")
        db_result = await client.execute_tool(
            'query_database',
            {'query': 'SELECT * FROM orders WHERE total > 1000', 'limit': 5}
        )
        
        await asyncio.sleep(2)
        
        # Step 3: Calculate metrics
        print("\n📍 PHASE 3: Business Metrics Calculation")
        print("-" * 40)
        print("Calculating revenue metrics...")
        metrics_result = await client.execute_tool(
            'calculate_metrics',
            {
                'metric_type': 'revenue',
                'date_range': {'start': '2024-01-01', 'end': '2024-12-31'}
            }
        )
        
        await asyncio.sleep(2)
        
        # Step 4: Analyze sentiment
        print("\n📍 PHASE 4: Sentiment Analysis")
        print("-" * 40)
        print("Analyzing customer feedback...")
        sentiment_result = await client.execute_tool(
            'analyze_sentiment',
            {'text': 'The product quality is excellent and the service was outstanding!'}
        )
        
        await asyncio.sleep(2)
        
        # Step 5: Send notification
        print("\n📍 PHASE 5: Customer Notification")
        print("-" * 40)
        print("Sending email notification...")
        
        if metrics_result.get('success'):
            revenue = metrics_result['result']['value']
            trend = metrics_result['result']['trend']
            
            email_result = await client.execute_tool(
                'send_email',
                {
                    'to': 'customer@example.com',
                    'subject': 'Monthly Business Report',
                    'body': f"Revenue: ${revenue:.2f}\nTrend: {trend}\nThank you for your business!"
                }
            )
        
        await asyncio.sleep(1)
        
        # Step 6: Check history
        print("\n📍 PHASE 6: Execution History")
        print("-" * 40)
        history = await client.get_history(limit=5)
        print(f"   Total Executions: {history['total']}")
        print(f"   Recent Tools Used:")
        for exec in history.get('recent', [])[:3]:
            print(f"      • {exec['tool']} at {exec['timestamp'][:19]}")
        
        print("\n" + "="*70)
        print(" "*15 + "✅ WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*70 + "\n")

async def simple_demo():
    """Run a simple MCP demo"""
    print("\n" + "="*60)
    print(" "*15 + "SIMPLE MCP DEMO")
    print("="*60)
    
    async with MCPClient() as client:
        # Just discover and execute one tool
        await client.discover_tools()
        
        print("\n📊 Executing weather check...")
        weather = await client.execute_tool(
            'get_weather',
            {'location': 'San Francisco', 'units': 'celsius'}
        )
        
        if weather.get('success'):
            result = weather['result']
            print(f"\n🌤️ Weather in {result['location']}:")
            print(f"   Temperature: {result['temperature']}°C")
            print(f"   Conditions: {result['conditions']}")
            print(f"   Humidity: {result['humidity']}%")
    
    print("\n✅ Demo Complete!\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'simple':
        asyncio.run(simple_demo())
    else:
        asyncio.run(demo_workflow())
