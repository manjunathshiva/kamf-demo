# ============================================

# flink-jobs/submit_job.sh
#!/bin/bash
# Script to submit Flink job

echo "Waiting for Flink to be ready..."
sleep 10

echo "Submitting Flink job..."
/opt/flink/bin/flink run -py /opt/flink/jobs/order_processor.py

echo "Job submitted successfully!"