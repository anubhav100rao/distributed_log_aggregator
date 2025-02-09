# log_generator.py
import os
import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer

# Environment variables for configuration
SERVICE_NAME = os.getenv("SERVICE_NAME", "default-service")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")
LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR"]

def generate_log_message():
    level = random.choice(LOG_LEVELS)
    timestamp = datetime.utcnow().isoformat()
    # Compose a structured log message
    message = {
        "timestamp": timestamp,
        "service": SERVICE_NAME,
        "level": level,
        "message": "This is a log message."
    }
    return message

if __name__ == "__main__":
    # Initialize the Kafka producer with JSON serialization
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Starting log generator for {SERVICE_NAME}, sending logs to {KAFKA_BROKER} on topic '{KAFKA_TOPIC}'")
    while True:
        log_message = generate_log_message()
        # Print to stdout for debugging/visibility
        print(json.dumps(log_message), flush=True)
        # Send the log message to Kafka
        producer.send(KAFKA_TOPIC, log_message)
        producer.flush()
        time.sleep(random.uniform(0.5, 2))
