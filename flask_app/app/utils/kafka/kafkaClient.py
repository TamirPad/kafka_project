from confluent_kafka import Producer, Consumer, KafkaError
from app.config import Config

class KafkaClient:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS


    def produce_message(self, topic: str, message: str) -> None:
        pass

    def consume_messages(self, topic: str) -> None:
        pass

    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        pass
