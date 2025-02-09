# log_consumer_batched.py
import json
import os
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers

# Configuration from environment
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")
ES_HOST = os.getenv("ES_HOST", "elasticsearch")
ES_PORT = os.getenv("ES_PORT", "9200")
ES_INDEX = os.getenv("ES_INDEX", "logs")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))
BATCH_TIMEOUT = float(os.getenv("BATCH_TIMEOUT", "5.0"))

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

es = Elasticsearch([{"host": ES_HOST, "port": ES_PORT}])

print("Starting batched log consumer...")

batch = []
last_flush = datetime.utcnow()

def flush_batch():
    global batch, last_flush
    if not batch:
        return
    try:
        helpers.bulk(es, batch)
        print(f"Flushed {len(batch)} documents")
    except Exception as e:
        print(f"Error indexing batch: {e}")
    batch = []
    last_flush = datetime.utcnow()

for message in consumer:
    log_data = message.value
    log_data["ingestion_time"] = datetime.utcnow().isoformat()

    # Prepare the document for bulk indexing
    action = {
        "_index": ES_INDEX,
        "_source": log_data,
    }
    batch.append(action)

    # Flush if the batch size is reached or timeout is exceeded
    if len(batch) >= BATCH_SIZE or (datetime.utcnow() - last_flush).total_seconds() >= BATCH_TIMEOUT:
        flush_batch()
