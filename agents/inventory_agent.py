# ============================================

# agents/inventory_agent.py
"""
Inventory Agent - Consumes orders and checks inventory
"""
import json
import time
import random
import os
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger('InventoryAgent')

class InventoryAgent:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.agent_name = os.getenv('AGENT_NAME', 'inventory-agent')
        
        # Wait for Kafka to be ready
        time.sleep(10)
        
        # Simulated inventory database
        self.inventory = {
            'Laptop': random.randint(5, 50),
            'Mouse': random.randint(20, 100),
            'Keyboard': random.randint(15, 75),
            'Monitor': random.randint(3, 30),
            'Headphones': random.randint(10, 60),
            'Webcam': random.randint(5, 40)
        }
        
        # Initialize Kafka producer for responses
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8') if v else None
        )
        
        # Initialize Kafka consumer for orders
        self.consumer = KafkaConsumer(
            'order-events',
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id=f'{self.agent_name}-group',
            auto_offset_reset='latest'
        )
        
        logger.info(f"Inventory Agent '{self.agent_name}' initialized")
        logger.info(f"Current inventory: {self.inventory}")
    
    def check_inventory(self, order):
        """Check if items in order are available"""
        available = True
        missing_items = []
        inventory_check = []
        
        for item in order['items']:
            product = item['product']
            quantity = item['quantity']
            
            if product in self.inventory:
                if self.inventory[product] >= quantity:
                    inventory_check.append({
                        'product': product,
                        'requested': quantity,
                        'available': self.inventory[product],
                        'status': 'in_stock'
                    })
                else:
                    available = False
                    missing_items.append(f"{product} (need {quantity}, have {self.inventory[product]})")
                    inventory_check.append({
                        'product': product,
                        'requested': quantity,
                        'available': self.inventory[product],
                        'status': 'insufficient_stock'
                    })
            else:
                available = False
                missing_items.append(f"{product} (not in catalog)")
                inventory_check.append({
                    'product': product,
                    'requested': quantity,
                    'available': 0,
                    'status': 'not_found'
                })
        
        return available, missing_items, inventory_check
    
    def process_order(self, order):
        """Process incoming order and check inventory"""
        logger.info(f"Processing order {order['order_id']}")
        
        # Visual indicator for demo
        print("\n" + "="*60)
        print(f"🔍 INVENTORY CHECK: {order['order_id']}")
        print(f"   Checking {len(order['items'])} items...")
        
        # Check inventory
        available, missing_items, inventory_check = self.check_inventory(order)
        
        # Create response
        response = {
            'order_id': order['order_id'],
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_name,
            'original_order': order,
            'inventory_status': 'available' if available else 'partial',
            'missing_items': missing_items,
            'inventory_details': inventory_check
        }
        
        # Display results
        for check in inventory_check:
            status_icon = "✅" if check['status'] == 'in_stock' else "⚠️"
            print(f"   {status_icon} {check['product']}: {check['requested']} requested, "
                  f"{check['available']} available")
        
        print(f"   Result: {'✅ All items available' if available else '❌ Some items unavailable'}")
        print("="*60 + "\n")
        
        # If everything is available, reserve the inventory
        if available:
            for item in order['items']:
                self.inventory[item['product']] -= item['quantity']
            logger.info(f"Reserved inventory for order {order['order_id']}")
        
        return response
    
    def publish_inventory_response(self, response):
        """Publish inventory check response to Kafka"""
        try:
            future = self.producer.send(
                'inventory-responses',
                key=response['order_id'],
                value=response
            )
            record_metadata = future.get(timeout=10)
            
            logger.info(f"✅ Published inventory response for {response['order_id']} "
                       f"to topic '{record_metadata.topic}'")
            
            return True
        except KafkaError as e:
            logger.error(f"Failed to publish inventory response: {e}")
            return False
    
    def run(self):
        """Main processing loop"""
        logger.info("Starting Inventory Agent...")
        logger.info("Listening for order events...")
        
        try:
            for message in self.consumer:
                order = message.value
                
                # Add small delay for demo visibility
                time.sleep(2)
                
                # Process the order
                response = self.process_order(order)
                
                # Publish response
                self.publish_inventory_response(response)
                
                # Occasionally replenish inventory (for demo)
                if random.random() < 0.3:
                    product = random.choice(list(self.inventory.keys()))
                    amount = random.randint(10, 30)
                    self.inventory[product] += amount
                    logger.info(f"📦 Replenished {product} by {amount} units")
                
        except KeyboardInterrupt:
            logger.info("Shutting down Inventory Agent...")
        except Exception as e:
            logger.error(f"Error in processing loop: {e}")
        finally:
            self.producer.close()

if __name__ == "__main__":
    agent = InventoryAgent()
    agent.run()