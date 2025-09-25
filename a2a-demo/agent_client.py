"""
A2A Protocol Demo - Client for testing agent communication
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('A2A-Client')

class A2AClient:
    """Client for A2A agent interaction"""
    
    def __init__(self, name: str = "demo-client"):
        self.name = name
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
    
    async def discover_agent(self, agent_url: str):
        """Discover agent capabilities"""
        print(f"\n🔍 Discovering agent at {agent_url}...")
        
        async with self.session.get(f"{agent_url}/a2a/discovery") as resp:
            if resp.status == 200:
                agent_card = await resp.json()
                
                print("\n" + "="*60)
                print("✅ AGENT DISCOVERED")
                print(f"   Name: {agent_card['name']}")
                print(f"   ID: {agent_card['agent_id']}")
                print(f"   Version: {agent_card['version']}")
                print(f"   Capabilities:")
                for cap in agent_card['capabilities']:
                    print(f"      • {cap}")
                print("="*60)
                
                return agent_card
            else:
                print(f"❌ Discovery failed: {resp.status}")
                return None
    
    async def request_task(self, agent_url: str, method: str, params: dict = None):
        """Submit task to agent"""
        request_id = str(uuid.uuid4())
        
        task_request = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': request_id,
            'from_agent': self.name
        }
        
        print(f"\n📤 Sending task: {method}")
        print(f"   Parameters: {json.dumps(params, indent=2)}")
        
        async with self.session.post(
            f"{agent_url}/a2a/tasks",
            json=task_request
        ) as resp:
            if resp.status == 200:
                result = await resp.json()
                task_id = result.get('result', {}).get('task_id')
                
                print(f"\n✅ Task accepted")
                print(f"   Task ID: {task_id}")
                
                return task_id
            else:
                print(f"❌ Task request failed: {resp.status}")
                return None
    
    async def check_task_status(self, agent_url: str, task_id: str):
        """Check task status"""
        async with self.session.get(f"{agent_url}/a2a/tasks/{task_id}") as resp:
            if resp.status == 200:
                return await resp.json()
            return None
    
    async def wait_for_completion(self, agent_url: str, task_id: str, timeout: int = 30):
        """Wait for task to complete"""
        print(f"\n⏳ Waiting for task completion...")
        
        start_time = asyncio.get_event_loop().time()
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            status = await self.check_task_status(agent_url, task_id)
            
            if status and status.get('status') == 'completed':
                print("\n" + "="*60)
                print("✅ TASK COMPLETED")
                print(f"   Duration: {status.get('completed_at', 'N/A')}")
                
                result = status.get('result', {})
                if 'artifacts' in result:
                    print(f"   Artifacts: {len(result['artifacts'])} generated")
                if 'analysis' in result:
                    print(f"   Analysis Results:")
                    for key, value in result['analysis'].items():
                        print(f"      • {key}: {value}")
                print("="*60)
                
                return status
            
            await asyncio.sleep(1)
            print(".", end="", flush=True)
        
        print("\n❌ Task timeout")
        return None

async def demo_workflow():
    """Run complete A2A demo workflow"""
    print("\n" + "="*70)
    print(" "*20 + "A2A PROTOCOL DEMO")
    print("="*70)
    
    agent_url = "http://localhost:5000"
    
    async with A2AClient() as client:
        # Step 1: Discovery
        print("\n📍 PHASE 1: Agent Discovery")
        print("-" * 40)
        agent = await client.discover_agent(agent_url)
        
        if not agent:
            print("Failed to discover agent")
            return
        
        await asyncio.sleep(2)
        
        # Step 2: Task Request
        print("\n📍 PHASE 2: Task Delegation")
        print("-" * 40)
        
        task_id = await client.request_task(
            agent_url,
            method='data_analysis',
            params={
                'dataset': 'sales_2024',
                'metrics': ['revenue', 'growth', 'churn'],
                'timeframe': 'Q4'
            }
        )
        
        if not task_id:
            print("Failed to submit task")
            return
        
        await asyncio.sleep(1)
        
        # Step 3: Monitor Completion
        print("\n📍 PHASE 3: Task Monitoring")
        print("-" * 40)
        
        result = await client.wait_for_completion(agent_url, task_id)
        
        if result:
            print("\n🎉 Demo completed successfully!")
        else:
            print("\n⚠️ Demo incomplete")
    
    print("\n" + "="*70)
    print(" "*15 + "END OF A2A DEMO")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(demo_workflow())
