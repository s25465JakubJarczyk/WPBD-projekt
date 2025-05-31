FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY load_data.py .
COPY customers.csv .
COPY products.csv .
COPY orders.csv .
COPY kafka_consumer.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "kafka_consumer.py"]
