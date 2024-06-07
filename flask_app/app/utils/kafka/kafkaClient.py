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


    def consume_messages(self, topic: str) -> None:
        """
        Consume messages from a Kafka topic.

        Args:
            topic (str): The topic to consume messages from.

        Raises:
            Exception: If an error occurs while consuming messages.
        """
        consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': 'foo',
            'auto.offset.reset': 'earliest'
        })


        try:
            consumer.subscribe([topic])

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
                    logging.info('Received message: {}'.format(msg.value().decode('utf-8')))
        except KeyboardInterrupt:
            raise Exception
        finally:
            consumer.close()
