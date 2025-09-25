# flink-jobs/order_processor.py
"""
Flink Job for Real-time Order Processing
Aggregates orders, detects patterns, and triggers alerts
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction, ProcessFunction
from pyflink.common.time import Time
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FlinkOrderProcessor')

class OrderEnricher(MapFunction):
    """Enrich order with additional metadata"""
    
    def map(self, order):
        # Parse order if it's a string
        if isinstance(order, str):
            order = json.loads(order)
        
        # Add enrichment
        order['processed_time'] = datetime.now().isoformat()
        order['processing_node'] = 'flink-processor-1'
        
        # Calculate order metrics
        order['item_count'] = len(order.get('items', []))
        order['avg_item_price'] = order.get('total', 0) / max(order['item_count'], 1)
        
        # Categorize order size
        total = order.get('total', 0)
        if total < 100:
            order['order_category'] = 'small'
        elif total < 500:
            order['order_category'] = 'medium'
        else:
            order['order_category'] = 'large'
        
        return order

class FraudDetector(ProcessFunction):
    """Detect potential fraudulent patterns"""
    
    def process_element(self, order, ctx):
        # Simple fraud detection rules
        fraud_score = 0
        fraud_reasons = []
        
        # Check for suspicious patterns
        if order.get('total', 0) > 5000:
            fraud_score += 30
            fraud_reasons.append('High value order')
        
        if order.get('item_count', 0) > 10:
            fraud_score += 20
            fraud_reasons.append('Unusual quantity')
        
        # Check velocity (would need state in real implementation)
        # For demo, just simulate
        if 'CUST-999' in order.get('customer_id', ''):
            fraud_score += 50
            fraud_reasons.append('Flagged customer')
        
        # Add fraud analysis to order
        order['fraud_score'] = fraud_score
        order['fraud_reasons'] = fraud_reasons
        order['requires_review'] = fraud_score > 40
        
        # Emit enriched order
        yield order
        
        # If high fraud score, emit alert
        if fraud_score > 40:
            alert = {
                'alert_type': 'fraud_detection',
                'order_id': order['order_id'],
                'fraud_score': fraud_score,
                'reasons': fraud_reasons,
                'timestamp': datetime.now().isoformat()
            }
            # In real implementation, this would go to a separate stream
            logger.warning(f"⚠️ FRAUD ALERT: Order {order['order_id']} has score {fraud_score}")

# OrderAggregator removed for simplified demo

def create_flink_job():
    """Create and configure Flink streaming job for order processing demo"""
    
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    # Configure checkpointing for fault tolerance
    env.enable_checkpointing(10000)  # Checkpoint every 10 seconds
    
    # Create dynamic sample order data stream (changes each run)
    import random
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam']
    sample_orders = []
    
    for i in range(random.randint(3, 6)):  # Variable number of orders
        product = random.choice(products)
        quantity = random.randint(1, 3)
        price = round(random.uniform(50, 2000), 2)
        total = quantity * price
        
        order = {
            'order_id': f'ORD-FLINK-{timestamp}-{i+1}',
            'customer_id': f'CUST-{random.randint(100, 999)}',
            'total': total,
            'timestamp': datetime.now().isoformat(),
            'items': [{'product': product, 'quantity': quantity, 'price': price}]
        }
        sample_orders.append(json.dumps(order))
    
    # Create data stream from sample orders
    order_stream = env.from_collection(sample_orders)
    
    # Apply transformations
    enriched_orders = order_stream \
        .map(OrderEnricher()) \
        .name("EnrichOrders")
    
    # Fraud detection branch
    fraud_checked = enriched_orders \
        .process(FraudDetector()) \
        .name("FraudDetection")
    
    # Print results for demo visibility
    fraud_checked.print()
    
    # Execute the job
    env.execute("KAMF Demo - Order Processing Pipeline")

if __name__ == "__main__":
    logger.info("Starting Flink Order Processing Job...")
    create_flink_job()




