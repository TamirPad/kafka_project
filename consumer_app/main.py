from elasticsearch import Elasticsearch
from confluent_kafka import Consumer, KafkaError
from deserialize.proto_order_serializer import ProtoOrderSerializer
import logging


logging.basicConfig(level=logging.INFO)

# Initialize Elasticsearch client
client = Elasticsearch("http://localhost:9200")

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': "localhost:9092",
    'group.id': '1',
    'auto.offset.reset': 'earliest'
})

# Subscribe to 'orders' topic
consumer.subscribe(['orders'])
logging.info("Subscribed to topic 'orders' ")

try:
    # Start consuming messages
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.info("End of partition reached {}/{}".format(msg.topic(), msg.partition()))
                continue
            else:
                logging.error("Kafka error: {}".format(msg.error()))
                break
        else:
            order = ProtoOrderSerializer.deserialize_order(msg.value())
            logging.info('Received message: {}'.format(order))

            # Index the order into Elasticsearch
            try:
                json_order = {
                        "id": order.id,
                        "customer_id": order.customer_id,
                        "product_ids": order.product_ids,
                        "created_date": order.created_date,
                        "updated_date": order.updated_date
                }

                client.index(index="orders", body=json_order)
            except Exception as e:
                logging.error("Error indexing order into Elasticsearch: {}".format(e))

except KeyboardInterrupt:
    logging.info("Consumer interrupted by user")
