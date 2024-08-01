from elasticsearch import Elasticsearch
from confluent_kafka import Consumer, KafkaError
from flask_app.app.utils.kafka.kafka_messages.serializers.proto_order_serializer import ProtoOrderSerializer
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
            order_message = ProtoOrderSerializer.deserialize_order(msg.value())
            logging.info('Received message: {}'.format(order_message))

            # Index the order into Elasticsearch
            try:
                if msg.HasField('order_created'):
                    json_msg = {
                        "message": "order_created",

                        "order": {
                            "id": order_message.order_created.order.id,
                            "customer_id": order_message.order_created.order.customer_id,
                            "product_ids": order_message.order_created.order.product_ids,
                            "created_date": order_message.order_created.order.created_date,
                            "updated_date": order_message.order_created.order.updated_date
                        }
                    }
                elif msg.HasField('order_updated'):
                    json_msg = {
                        "message": "order_updated",

                        "order": {
                            "id": order_message.order_updated.order.id,
                            "customer_id": order_message.order_updated.order.customer_id,
                            "product_ids": order_message.order_updated.order.product_ids,
                            "created_date": order_message.order_updated.order.created_date,
                            "updated_date": order_message.order_updated.order.updated_date
                        }
                    }
                elif msg.HasField('order_deleted'):
                    json_msg = {
                        "message": "order_deleted",
                        "order_id": order_message.order_deleted.order.id,
                    }
                else:
                    raise ValueError

                print(json_msg)
                client.index(index="orders", body=json_msg)
            except Exception as e:
                logging.error("Error indexing order into Elasticsearch: {}".format(e))

except KeyboardInterrupt:
    logging.info("Consumer interrupted by user")
