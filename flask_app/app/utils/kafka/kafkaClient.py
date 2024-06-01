from confluent_kafka import Producer, Consumer, KafkaError
from config import Config

class KafkaClient:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS


    def produce_message(self, topic: str, message: str) -> None:
        pass

    def consume_messages(self, topic: str) -> None:

        consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': 'foo',
            'auto.offset.reset': 'earliest'
        })

        consumer.subscribe([topic])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                else:
                    print('Received message: {}'.format(msg.value().decode('utf-8')))
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
        pass

# Example usage:
if __name__ == "__main__":
    
    kafka_client = KafkaClient('localhost:9092')
    
    # Consume messages from a topic
    kafka_client.consume_messages('orders')