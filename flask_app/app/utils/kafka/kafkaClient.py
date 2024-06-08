from confluent_kafka import Producer, Consumer, KafkaError
import json
import logging

class KafkaClient:
    """
    A class to interact with Kafka.

    Attributes:
        bootstrap_servers (str): The comma-separated list of broker addresses.
    """

    def __init__(self, bootstrap_servers: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        logging.info("KafkaClient initialized successfully")



    def produce_message(self, topic: str, message: str) -> None:
        """
        Produce a message to a Kafka topic.

        Args:
            topic (str): The topic to produce the message to.
            message (str): The message to be produced.

        Raises:
            Exception: If an error occurs while producing the message.
        """
        producer = Producer({'bootstrap.servers': self.bootstrap_servers})

        try:
            producer.produce(topic, message)
            producer.flush()
            logging.info("Message sent successfully")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise Exception

