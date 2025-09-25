# agents/order_agent.py
"""
Order Processing Agent - Publishes order events to Kafka
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
logger = logging.getLogger('OrderAgent')

class OrderAgent:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.agent_name = os.getenv('AGENT_NAME', 'order-agent')
        
        # Wait for Kafka to be ready
        time.sleep(10)
        
        # Initialize Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8') if v else None
        )
        
        # Initialize Kafka consumer for inventory responses
        self.consumer = KafkaConsumer(
            'inventory-responses',
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id=f'{self.agent_name}-group',
            auto_offset_reset='latest'
        )
        
        logger.info(f"Order Agent '{self.agent_name}' initialized")
    
    def create_order(self, order_id=None):
        """Create a new order and publish to Kafka"""
        if not order_id:
            order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        
        # Sample products
        products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam']
        
        order = {
            'order_id': order_id,
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_name,
            'customer_id': f"CUST-{random.randint(1, 1000)}",
            'items': [
                {
                    'product': random.choice(products),
                    'quantity': random.randint(1, 5),
                    'price': round(random.uniform(10, 500), 2)
                }
                for _ in range(random.randint(1, 3))
            ],
            'status': 'pending_inventory_check'
        }
        
        # Calculate total
        order['total'] = sum(item['quantity'] * item['price'] for item in order['items'])
        
        return order
    
    def publish_order(self, order):
        """Publish order to Kafka"""
        try:
            future = self.producer.send(
                'order-events',
                key=order['order_id'],
                value=order
            )
            record_metadata = future.get(timeout=10)
            
            logger.info(f"✅ Published order {order['order_id']} to topic '{record_metadata.topic}' "
                       f"partition {record_metadata.partition} offset {record_metadata.offset}")
            
            # Visual indicator for demo
            print("\n" + "="*60)
            print(f"📦 ORDER CREATED: {order['order_id']}")
            print(f"   Customer: {order['customer_id']}")
            print(f"   Items: {len(order['items'])} items")
            print(f"   Total: ${order['total']:.2f}")
            print("="*60 + "\n")
            
            return True
        except KafkaError as e:
            logger.error(f"Failed to publish order: {e}")
            return False
    
    def listen_for_inventory_responses(self):
        """Listen for inventory check responses"""
        logger.info("Listening for inventory responses...")
        
        for message in self.consumer:
            response = message.value
            
            # Visual indicator for demo
            print("\n" + "="*60)
            print(f"📥 INVENTORY RESPONSE RECEIVED")
            print(f"   Order: {response.get('order_id')}")
            print(f"   Status: {response.get('inventory_status')}")
            
            if response.get('inventory_status') == 'available':
                print(f"   ✅ All items in stock!")
                # Could trigger next step: payment processing
                self.publish_order_confirmation(response['order_id'])
            else:
                print(f"   ❌ Some items out of stock")
                missing = response.get('missing_items', [])
                for item in missing:
                    print(f"      - {item}")
            
            print("="*60 + "\n")
    
    def publish_order_confirmation(self, order_id):
        """Publish order confirmation event"""
        confirmation = {
            'order_id': order_id,
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_name,
            'status': 'confirmed',
            'next_step': 'payment_processing'
        }
        
        self.producer.send('order-confirmations', key=order_id, value=confirmation)
        logger.info(f"Published confirmation for order {order_id}")
    
    def run_demo_loop(self):
        """Run continuous demo loop"""
        logger.info("Starting Order Agent demo loop...")
        
        # Start a thread to listen for responses
        import threading
        listener_thread = threading.Thread(target=self.listen_for_inventory_responses)
        listener_thread.daemon = True
        listener_thread.start()
        
        while True:
            try:
                # Create and publish a new order every 15 seconds
                order = self.create_order()
                self.publish_order(order)
                
                # Wait before next order
                time.sleep(15)
                
            except KeyboardInterrupt:
                logger.info("Shutting down Order Agent...")
                break
            except Exception as e:
                logger.error(f"Error in demo loop: {e}")
                time.sleep(5)
        
        self.producer.close()

if __name__ == "__main__":
    agent = OrderAgent()
    agent.run_demo_loop()




