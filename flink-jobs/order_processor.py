# flink-jobs/order_processor.py
"""
Flink Job for Real-time Order Processing
Aggregates orders, detects patterns, and triggers alerts
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer, KafkaSink, KafkaRecordSerializationSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema, JsonRowSerializationSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import MapFunction, ProcessWindowFunction, ProcessFunction
from pyflink.datastream.window import TumblingEventTimeWindows, SlidingEventTimeWindows
from pyflink.common.time import Time
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.table import StreamTableEnvironment
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

class OrderAggregator(ProcessWindowFunction):
    """Aggregate orders in time windows"""
    
    def process(self, key, context, elements):
        orders = list(elements)
        
        # Calculate window statistics
        window_stats = {
            'window_start': datetime.fromtimestamp(context.window().start / 1000).isoformat(),
            'window_end': datetime.fromtimestamp(context.window().end / 1000).isoformat(),
            'order_count': len(orders),
            'total_revenue': sum(o.get('total', 0) for o in orders),
            'avg_order_value': sum(o.get('total', 0) for o in orders) / max(len(orders), 1),
            'unique_customers': len(set(o.get('customer_id') for o in orders)),
            'product_summary': self._get_product_summary(orders),
            'timestamp': datetime.now().isoformat()
        }
        
        yield window_stats
    
    def _get_product_summary(self, orders):
        product_counts = {}
        for order in orders:
            for item in order.get('items', []):
                product = item.get('product')
                if product:
                    product_counts[product] = product_counts.get(product, 0) + item.get('quantity', 0)
        return product_counts

def create_flink_job():
    """Create and configure Flink streaming job"""
    
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    
    # Configure checkpointing for fault tolerance
    env.enable_checkpointing(10000)  # Checkpoint every 10 seconds
    
    # Create Kafka source for orders
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("kafka:29092") \
        .set_topics("order-events") \
        .set_group_id("flink-order-processor") \
        .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
        .set_value_only_deserializer(
            JsonRowDeserializationSchema.builder()
                .type_info(Types.MAP(Types.STRING(), Types.PRIMITIVE()))
                .build()
        ) \
        .build()
    
    # Create the main processing pipeline
    order_stream = env.from_source(
        kafka_source,
        WatermarkStrategy.for_monotonous_timestamps(),
        "KafkaOrderSource"
    )
    
    # Apply transformations
    enriched_orders = order_stream \
        .map(OrderEnricher()) \
        .name("EnrichOrders")
    
    # Fraud detection branch
    fraud_checked = enriched_orders \
        .process(FraudDetector()) \
        .name("FraudDetection")
    
    # Window aggregation branch (every 30 seconds)
    windowed_stats = enriched_orders \
        .key_by(lambda x: "all") \
        .window(TumblingEventTimeWindows.of(Time.seconds(30))) \
        .process(OrderAggregator()) \
        .name("WindowAggregation")
    
    # Create Kafka sinks
    enriched_sink = KafkaSink.builder() \
        .set_bootstrap_servers("kafka:29092") \
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
                .set_topic("enriched-orders")
                .set_value_serialization_schema(
                    JsonRowSerializationSchema.builder()
                        .with_type_info(Types.MAP(Types.STRING(), Types.PRIMITIVE()))
                        .build()
                )
                .build()
        ) \
        .build()
    
    stats_sink = KafkaSink.builder() \
        .set_bootstrap_servers("kafka:29092") \
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
                .set_topic("order-statistics")
                .set_value_serialization_schema(
                    JsonRowSerializationSchema.builder()
                        .with_type_info(Types.MAP(Types.STRING(), Types.PRIMITIVE()))
                        .build()
                )
                .build()
        ) \
        .build()
    
    # Send processed streams to Kafka
    fraud_checked.sink_to(enriched_sink).name("EnrichedOrdersSink")
    windowed_stats.sink_to(stats_sink).name("StatisticsSink")
    
    # Print to console for demo visibility
    fraud_checked.print()
    windowed_stats.print()
    
    # Execute the job
    env.execute("Order Processing Pipeline")

if __name__ == "__main__":
    logger.info("Starting Flink Order Processing Job...")
    create_flink_job()




