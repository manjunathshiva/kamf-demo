"""
A2A Protocol Demo - Complete Agent Server Implementation
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from aiohttp import web
from dataclasses import dataclass, asdict
import uuid
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger('A2A-Server')

@dataclass
class AgentCard:
    """Agent capability descriptor"""
    agent_id: str
    name: str
    description: str
    version: str
    capabilities: List[str]
    supported_protocols: List[str]
    endpoints: Dict[str, str]
    metadata: Dict[str, Any]

class A2AAgent:
    """A2A Protocol Agent Server"""
    
    def __init__(self, agent_id: str = None, name: str = "DataAnalyzer", port: int = 5000):
        self.agent_id = agent_id or f"agent-{uuid.uuid4().hex[:8]}"
        self.name = name
        self.port = port
        self.active_tasks = {}
        self.peer_agents = {}
        
        # Define capabilities based on agent type
        capabilities_map = {
            "DataAnalyzer": ["data_analysis", "statistical_modeling", "anomaly_detection"],
            "ReportGenerator": ["report_creation", "visualization", "pdf_export"],
            "OrderProcessor": ["order_validation", "inventory_check", "payment_processing"]
        }
        
        self.agent_card = AgentCard(
            agent_id=self.agent_id,
            name=name,
            description=f"A2A-enabled {name} agent for collaborative processing",
            version="1.0.0",
            capabilities=capabilities_map.get(name, ["general_processing"]),
            supported_protocols=["a2a/v1", "json-rpc/2.0"],
            endpoints={
                "discovery": f"http://localhost:{port}/a2a/discovery",
                "tasks": f"http://localhost:{port}/a2a/tasks",
                "status": f"http://localhost:{port}/a2a/status"
            },
            metadata={
                "created_at": datetime.now().isoformat(),
                "status": "active",
                "performance": {"avg_response_time_ms": 250}
            }
        )
        
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configure HTTP routes"""
        self.app.router.add_get('/a2a/discovery', self.handle_discovery)
        self.app.router.add_post('/a2a/tasks', self.handle_task_request)
        self.app.router.add_get('/a2a/tasks/{task_id}', self.handle_task_status)
        self.app.router.add_get('/a2a/status', self.handle_status)
        self.app.router.add_post('/a2a/register', self.handle_peer_registration)
    
    async def handle_discovery(self, request):
        """Return agent capabilities via AgentCard"""
        print("\n" + "="*60)
        print(f"🔍 A2A DISCOVERY REQUEST")
        print(f"   Agent: {self.name}")
        print(f"   ID: {self.agent_id}")
        print(f"   Capabilities: {', '.join(self.agent_card.capabilities)}")
        print("="*60 + "\n")
        
        return web.json_response(asdict(self.agent_card))
    
    async def handle_task_request(self, request):
        """Process incoming task via JSON-RPC"""
        data = await request.json()
        
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id', str(uuid.uuid4()))
        from_agent = data.get('from_agent', 'unknown')
        
        print("\n" + "="*60)
        print(f"📋 A2A TASK REQUEST")
        print(f"   Method: {method}")
        print(f"   From: {from_agent}")
        print(f"   Request ID: {request_id}")
        print("="*60 + "\n")
        
        # Validate method is supported
        if method not in self.agent_card.capabilities:
            return web.json_response({
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {'code': -32601, 'message': f'Method {method} not supported'}
            }, status=400)
        
        # Create and start task
        task = {
            'id': request_id,
            'method': method,
            'params': params,
            'status': 'processing',
            'started_at': datetime.now().isoformat()
        }
        self.active_tasks[request_id] = task
        
        # Process async
        asyncio.create_task(self._process_task(task))
        
        return web.json_response({
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'task_id': request_id,
                'status': 'accepted',
                'estimated_time': '3-5 seconds'
            }
        })
    
    async def _process_task(self, task):
        """Simulate task processing"""
        await asyncio.sleep(random.uniform(2, 4))
        
        # Generate results based on method
        if task['method'] == 'data_analysis':
            result = {
                'dataset': task['params'].get('dataset', 'unknown'),
                'metrics': task['params'].get('metrics', []),
                'analysis': {
                    'total_records': random.randint(1000, 10000),
                    'anomalies': random.randint(0, 50),
                    'confidence': round(random.uniform(0.85, 0.99), 2)
                },
                'artifacts': [
                    {'type': 'report', 'url': f"/reports/{task['id']}.pdf"},
                    {'type': 'data', 'url': f"/data/{task['id']}.json"}
                ]
            }
        else:
            result = {
                'status': 'completed',
                'output': f"Processed {task['method']} successfully",
                'duration_ms': random.randint(2000, 5000)
            }
        
        task['status'] = 'completed'
        task['result'] = result
        task['completed_at'] = datetime.now().isoformat()
        
        print("\n" + "="*60)
        print(f"✅ TASK COMPLETED")
        print(f"   Task ID: {task['id']}")
        print(f"   Method: {task['method']}")
        print("="*60 + "\n")
    
    async def handle_task_status(self, request):
        """Return task status and results"""
        task_id = request.match_info['task_id']
        task = self.active_tasks.get(task_id)
        
        if not task:
            return web.json_response({'error': 'Task not found'}, status=404)
        
        return web.json_response(task)
    
    async def handle_status(self, request):
        """Return agent status"""
        return web.json_response({
            'agent_id': self.agent_id,
            'name': self.name,
            'status': 'active',
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len([t for t in self.active_tasks.values() if t['status'] == 'completed']),
            'uptime': datetime.now().isoformat()
        })
    
    async def handle_peer_registration(self, request):
        """Register peer agent for collaboration"""
        data = await request.json()
        agent_card = data.get('agent_card')
        
        if agent_card:
            agent_id = agent_card.get('agent_id')
            self.peer_agents[agent_id] = agent_card
            
            print("\n" + "="*60)
            print(f"🤝 PEER REGISTERED")
            print(f"   Name: {agent_card.get('name')}")
            print(f"   Capabilities: {', '.join(agent_card.get('capabilities', []))}")
            print("="*60 + "\n")
            
            return web.json_response({'status': 'registered', 'agent_id': agent_id})
        
        return web.json_response({'error': 'Invalid agent card'}, status=400)
    
    def run(self):
        """Start the A2A agent server"""
        print(f"\n{'='*60}")
        print(f"🚀 A2A AGENT STARTING")
        print(f"   Name: {self.name}")
        print(f"   ID: {self.agent_id}")
        print(f"   Port: {self.port}")
        print(f"   Capabilities: {', '.join(self.agent_card.capabilities)}")
        print(f"{'='*60}\n")
        
        web.run_app(self.app, host='0.0.0.0', port=self.port)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    name = sys.argv[2] if len(sys.argv) > 2 else "DataAnalyzer"
    
    agent = A2AAgent(name=name, port=port)
    agent.run()
