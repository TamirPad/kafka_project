from flask_app.app.utils.kafka.kafkaClient import KafkaClient
from flask_app.app.dao.orders_dao import OrderDao
from flask_app.app.models.order import Order
from flask_app.app.utils.kafka.kafka_messages.serializers.proto_order_serializer import ProtoOrderSerializer
from flask_app.app.config import Config
import logging


class OrderService:
    def __init__(self, kafka_client: KafkaClient, order_dao: OrderDao):
        self.kafka_client = kafka_client
        self.kafka_topic = Config.KAFKA_TOPIC
        self.order_dao = order_dao
        logging.info("OrderService initialized successfully")

    def create_order(self, order: Order) -> bool:
        try:
            logging.info(f"[OrderService.create_order] Creating order with ID: {order.id}")
            self.order_dao.create_order(order)
            serialized_order = ProtoOrderSerializer.serialize_order(order,"create")
            self.kafka_client.produce_message(self.kafka_topic, serialized_order)
            logging.info(f"[OrderService.create_order] Order created and Kafka message produced for order ID: {order.id}")
        except Exception as e:
            logging.error(f"[OrderService.create_order] Failed to create order: {e}")
            raise

    def update_order(self, order: Order) -> bool:
        try:
            logging.info(f"[OrderService.update_order]Updating order with ID: {order.id}")
            affected_rows = self.order_dao.update_order(order)
            if affected_rows == 0:
                return False
            else:
                serialized_order = ProtoOrderSerializer.serialize_order(order, "update")
                self.kafka_client.produce_message(self.kafka_topic, serialized_order)
                logging.info(f"[OrderService.update_order] Order updated and Kafka message produced for order ID: {order.id}")
                return True
        except Exception as e:
            logging.error(f"[OrderService.update_order] Failed to update order: {e}")
            raise

    def delete_order(self, order: Order) -> bool:
        try:
            logging.info(f"[OrderService.delete_order] Deleting order with ID: {order.id}")
            affected_rows = self.order_dao.delete_order(order)
            if affected_rows == 0:
                return False
            else:
                serialized_order = ProtoOrderSerializer.serialize_order(order, "delete")
                self.kafka_client.produce_message(self.kafka_topic, serialized_order)
                logging.info(f"[OrderService.delete_order] Order deleted and Kafka message produced for order ID: {order.id}")
                return True
        except Exception as e:
            logging.error(f"[OrderService.delete_order] Failed to delete order: {e}")
            raise 

