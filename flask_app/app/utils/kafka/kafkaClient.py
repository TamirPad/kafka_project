from confluent_kafka import Producer, Consumer, KafkaError
import json
import logging

class KafkaClient:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers


    def produce_message(self, topic: str, message: str) -> None:
        producer = Producer({'bootstrap.servers': self.bootstrap_servers})

        try:
            producer.produce(topic, json.dumps(message).encode('utf-8'))
            producer.flush()
            logging.info("Message sent successfully")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise Exception
    


    def consume_messages(self, topic: str) -> None:

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

