from app.utils.kafka.kafkaClient import KafkaClient
from app.dao.orders_dao import Order, OrderDao
from app.utils.kafka.kafka_messages.serializers.proto_order_serializer import ProtoOrderSerializer
from app.config import Config
import logging


class OrderService:
    def __init__(self, kafka_client: KafkaClient, order_dao: OrderDao):
        self.kafka_client = kafka_client
        self.kafka_topic = Config.KAFKA_TOPIC
        self.order_dao = order_dao
        logging.info("OrderService initialized successfully")

    def create_order(self, order: Order) -> bool:
        try:
            logging.info(f"Creating order with ID: {order.id}")
            self.order_dao.create_order(order)
            serialized_order = ProtoOrderSerializer.serialize_order(order)
            self.kafka_client.produce_message(self.kafka_topic, serialized_order)
            logging.info(f"Order created and Kafka message produced for order ID: {order.id}")
        except Exception as e:
            logging.error(f"Failed to create order: {e}")

    def update_order(self, order: Order) -> bool:
        try:
            logging.info(f"Updating order with ID: {order.id}")
            self.order_dao.update_order(order)
            serialized_order = ProtoOrderSerializer.serialize_order(order)
            self.kafka_client.produce_message(self.kafka_topic, serialized_order)
            logging.info(f"Order updated and Kafka message produced for order ID: {order.id}")
        except Exception as e:
            logging.error(f"Failed to update order: {e}")

    def delete_order(self, order: Order) -> bool:
        try:
            logging.info(f"Deleting order with ID: {order.id}")
            self.order_dao.delete_order(order)
            serialized_order = ProtoOrderSerializer.serialize_order(order)
            self.kafka_client.produce_message(self.kafka_topic, serialized_order)
            logging.info(f"Order deleted and Kafka message produced for order ID: {order.id}")
        except Exception as e:
            logging.error(f"Failed to delete order: {e}")
