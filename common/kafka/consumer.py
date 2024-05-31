import logging
from kafka import KafkaConsumer
import config
from config import Config
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def consume_orders(topic_name, bootstrap_servers):
    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="earliest",  # Start consuming from the earliest message
            enable_auto_commit=True,  # Auto commit offsets
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in consumer:
            order = message.value
            logger.info(f'Consumed order: {order}')
    except Exception as e:
        logger.error(f"Error occurred while consuming orders: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    topic_name = Config.KAFKA_TOPIC
    bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS
    consume_orders(topic_name, bootstrap_servers)
