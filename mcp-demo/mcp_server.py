"""
MCP (Model Context Protocol) Demo - Complete Server Implementation
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
from aiohttp import web
import random
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger('MCP-Server')

@dataclass
class Tool:
    """MCP Tool Definition"""
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]
    examples: List[Dict[str, Any]]
    category: str

class MCPServer:
    """MCP Protocol Server Implementation"""
    
    def __init__(self, port: int = 6000):
        self.port = port
        self.tools = self._initialize_tools()
        self.context_store = {}
        self.execution_history = []
        
        # Setup web server
        self.app = web.Application()
        self._setup_routes()
    
    def _initialize_tools(self) -> Dict[str, Tool]:
        """Initialize available tools"""
        tools = {
            'query_database': Tool(
                name='query_database',
                description='Query the customer database',
                parameters={
                    'type': 'object',
                    'properties': {
                        'query': {'type': 'string', 'description': 'SQL query'},
                        'limit': {'type': 'integer', 'default': 100}
                    },
                    'required': ['query']
                },
                returns={'type': 'array', 'items': {'type': 'object'}},
                examples=[
                    {'query': 'SELECT * FROM orders WHERE total > 1000', 'limit': 10}
                ],
                category='data_access'
            ),
            
            'send_email': Tool(
                name='send_email',
                description='Send an email notification',
                parameters={
                    'type': 'object',
                    'properties': {
                        'to': {'type': 'string', 'format': 'email'},
                        'subject': {'type': 'string'},
                        'body': {'type': 'string'},
                        'cc': {'type': 'array', 'items': {'type': 'string'}}
                    },
                    'required': ['to', 'subject', 'body']
                },
                returns={'type': 'object', 'properties': {'success': {'type': 'boolean'}}},
                examples=[
                    {
                        'to': 'customer@example.com',
                        'subject': 'Order Confirmation',
                        'body': 'Your order has been confirmed.'
                    }
                ],
                category='communication'
            ),
            
            'calculate_metrics': Tool(
                name='calculate_metrics',
                description='Calculate business metrics',
                parameters={
                    'type': 'object',
                    'properties': {
                        'metric_type': {
                            'type': 'string',
                            'enum': ['revenue', 'conversion', 'churn', 'ltv']
                        },
                        'date_range': {
                            'type': 'object',
                            'properties': {
                                'start': {'type': 'string', 'format': 'date'},
                                'end': {'type': 'string', 'format': 'date'}
                            }
                        }
                    },
                    'required': ['metric_type']
                },
                returns={'type': 'object'},
                examples=[
                    {
                        'metric_type': 'revenue',
                        'date_range': {'start': '2024-01-01', 'end': '2024-12-31'}
                    }
                ],
                category='analytics'
            ),
            
            'get_weather': Tool(
                name='get_weather',
                description='Get weather information',
                parameters={
                    'type': 'object',
                    'properties': {
                        'location': {'type': 'string'},
                        'units': {'type': 'string', 'enum': ['celsius', 'fahrenheit']}
                    },
                    'required': ['location']
                },
                returns={'type': 'object'},
                examples=[
                    {'location': 'San Francisco', 'units': 'celsius'}
                ],
                category='external_api'
            ),
            
            'analyze_sentiment': Tool(
                name='analyze_sentiment',
                description='Analyze text sentiment',
                parameters={
                    'type': 'object',
                    'properties': {
                        'text': {'type': 'string'},
                        'language': {'type': 'string', 'default': 'en'}
                    },
                    'required': ['text']
                },
                returns={'type': 'object', 'properties': {'sentiment': {'type': 'string'}, 'score': {'type': 'number'}}},
                examples=[
                    {'text': 'I love this product!', 'language': 'en'}
                ],
                category='nlp'
            )
        }
        
        return tools
    
    def _setup_routes(self):
        """Setup MCP protocol routes"""
        self.app.router.add_get('/mcp/tools', self.handle_list_tools)
        self.app.router.add_get('/mcp/tools/{tool_name}', self.handle_get_tool)
        self.app.router.add_post('/mcp/tools/{tool_name}/execute', self.handle_execute_tool)
        self.app.router.add_post('/mcp/context', self.handle_set_context)
        self.app.router.add_get('/mcp/context', self.handle_get_context)
        self.app.router.add_get('/mcp/history', self.handle_get_history)
        self.app.router.add_get('/mcp/health', self.handle_health)
    
    async def handle_list_tools(self, request):
        """List all available tools"""
        logger.info("Listing all tools")
        
        # Visual demo output
        print("\n" + "="*60)
        print(f"📋 MCP TOOLS CATALOG REQUEST")
        print(f"   Available Tools: {len(self.tools)}")
        for name, tool in self.tools.items():
            print(f"      • {name}: {tool.description}")
        print("="*60 + "\n")
        
        tools_list = [asdict(tool) for tool in self.tools.values()]
        return web.json_response({
            'tools': tools_list,
            'count': len(tools_list),
            'categories': list(set(t.category for t in self.tools.values()))
        })
    
    async def handle_get_tool(self, request):
        """Get specific tool details"""
        tool_name = request.match_info['tool_name']
        tool = self.tools.get(tool_name)
        
        if not tool:
            return web.json_response({'error': f'Tool {tool_name} not found'}, status=404)
        
        # Visual demo output
        print("\n" + "="*60)
        print(f"🔧 MCP TOOL DETAILS REQUEST")
        print(f"   Tool: {tool.name}")
        print(f"   Category: {tool.category}")
        print(f"   Parameters: {len(tool.parameters.get('properties', {}))}")
        print("="*60 + "\n")
        
        return web.json_response(asdict(tool))
    
    async def handle_execute_tool(self, request):
        """Execute a tool with given parameters"""
        tool_name = request.match_info['tool_name']
        tool = self.tools.get(tool_name)
        
        if not tool:
            return web.json_response({'error': f'Tool {tool_name} not found'}, status=404)
        
        # Parse request
        data = await request.json()
        parameters = data.get('parameters', {})
        context = data.get('context', {})
        
        # Visual demo output
        print("\n" + "="*60)
        print(f"⚡ MCP TOOL EXECUTION REQUEST")
        print(f"   Tool: {tool_name}")
        print(f"   Parameters: {json.dumps(parameters, indent=2)}")
        if context:
            print(f"   Context Keys: {list(context.keys())}")
        print("="*60 + "\n")
        
        # Validate parameters (simplified)
        required = tool.parameters.get('required', [])
        for req in required:
            if req not in parameters:
                return web.json_response({
                    'error': f'Missing required parameter: {req}'
                }, status=400)
        
        # Execute tool (simulated)
        try:
            result = await self._execute_tool(tool_name, parameters, context)
            
            # Log execution
            execution = {
                'id': str(uuid.uuid4()),
                'tool': tool_name,
                'parameters': parameters,
                'context': context,
                'result': result,
                'timestamp': datetime.now().isoformat(),
                'execution_time_ms': random.randint(50, 500)
            }
            self.execution_history.append(execution)
            
            # Visual demo output
            print("\n" + "="*60)
            print(f"✅ MCP TOOL EXECUTION COMPLETE")
            print(f"   Tool: {tool_name}")
            print(f"   Status: Success")
            print(f"   Execution Time: {execution['execution_time_ms']}ms")
            print("="*60 + "\n")
            
            return web.json_response({
                'success': True,
                'result': result,
                'execution_id': execution['id'],
                'execution_time_ms': execution['execution_time_ms']
            })
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def _execute_tool(self, tool_name: str, parameters: Dict, context: Dict) -> Any:
        """Simulate tool execution"""
        
        # Simulate async work
        await asyncio.sleep(0.5)
        
        # Return mock results based on tool
        if tool_name == 'query_database':
            return [
                {'order_id': 'ORD-001', 'customer': 'Alice', 'total': 1500, 'status': 'completed'},
                {'order_id': 'ORD-002', 'customer': 'Bob', 'total': 2300, 'status': 'pending'},
                {'order_id': 'ORD-003', 'customer': 'Charlie', 'total': 1800, 'status': 'completed'}
            ]
        
        elif tool_name == 'send_email':
            return {
                'message_id': f'msg-{uuid.uuid4().hex[:8]}',
                'status': 'sent',
                'timestamp': datetime.now().isoformat(),
                'recipients': 1
            }
        
        elif tool_name == 'calculate_metrics':
            metric_type = parameters.get('metric_type')
            return {
                'metric': metric_type,
                'value': round(random.uniform(10000, 100000), 2),
                'change_percent': round(random.uniform(-10, 20), 2),
                'period': parameters.get('date_range', {}),
                'trend': random.choice(['increasing', 'decreasing', 'stable'])
            }
        
        elif tool_name == 'get_weather':
            return {
                'location': parameters.get('location'),
                'temperature': random.randint(15, 30),
                'conditions': random.choice(['sunny', 'cloudy', 'rainy', 'partly cloudy']),
                'humidity': random.randint(40, 80),
                'wind_speed': random.randint(5, 25)
            }
        
        elif tool_name == 'analyze_sentiment':
            sentiments = ['positive', 'negative', 'neutral']
            return {
                'text': parameters.get('text')[:50] + '...' if len(parameters.get('text', '')) > 50 else parameters.get('text'),
                'sentiment': random.choice(sentiments),
                'score': round(random.uniform(0, 1), 3),
                'confidence': round(random.uniform(0.7, 0.99), 2)
            }
        
        return {'status': 'completed'}
    
    async def handle_set_context(self, request):
        """Set context for tool execution"""
        data = await request.json()
        context_key = data.get('key')
        context_value = data.get('value')
        
        if context_key:
            self.context_store[context_key] = {
                'value': context_value,
                'updated_at': datetime.now().isoformat()
            }
            
            logger.info(f"Context updated: {context_key}")
            return web.json_response({
                'success': True,
                'message': f'Context {context_key} updated'
            })
        
        return web.json_response({'error': 'Context key required'}, status=400)
    
    async def handle_get_context(self, request):
        """Get current context"""
        return web.json_response({
            'context': self.context_store,
            'count': len(self.context_store)
        })
    
    async def handle_get_history(self, request):
        """Get execution history"""
        limit = int(request.query.get('limit', 10))
        history = self.execution_history[-limit:]
        
        return web.json_response({
            'history': history,
            'total': len(self.execution_history),
            'recent': history
        })
    
    async def handle_health(self, request):
        """Health check endpoint"""
        return web.json_response({
            'status': 'healthy',
            'tools_available': len(self.tools),
            'executions_total': len(self.execution_history),
            'context_keys': len(self.context_store),
            'uptime': datetime.now().isoformat()
        })
    
    def run(self):
        """Start the MCP server"""
        print(f"\n{'='*60}")
        print(f"🚀 MCP SERVER STARTING")
        print(f"   Port: {self.port}")
        print(f"   Tools Available: {len(self.tools)}")
        print(f"   Categories: {list(set(t.category for t in self.tools.values()))}")
        print(f"   Endpoints:")
        print(f"      • GET  /mcp/tools - List all tools")
        print(f"      • POST /mcp/tools/{{tool}}/execute - Execute tool")
        print(f"      • GET  /mcp/context - Get context")
        print(f"      • GET  /mcp/history - Execution history")
        print(f"{'='*60}\n")
        
        web.run_app(self.app, host='0.0.0.0', port=self.port)

if __name__ == "__main__":
    server = MCPServer()
    server.run()
