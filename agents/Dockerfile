# ============================================

# agents/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command can be overridden
CMD ["python", "order_agent.py"]