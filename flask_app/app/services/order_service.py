from app.utils.kafka.kafka_messages.generated import order_event_pb2
from app.utils.kafka.kafkaClient import KafkaClient
from app.dao.orders_dao import Order
from app.config import Config
import logging

class OrderService:
    def __init__(self, kafka_client: KafkaClient):
        self.kafka_client = kafka_client
        self.kafka_topic = Config.KAFKA_TOPIC

    def create_order(self, order: Order) -> bool:
        proto_order = self._serialize_order(order)
        logging.info("Order serialized successfully.")
        
        return self._send_to_kafka(proto_order, "create")

    def update_order(self, order: Order) -> bool:
        proto_order = self._serialize_order(order)
        logging.info("Order serialized successfully.")
        
        return self._send_to_kafka(proto_order, "update")

    def delete_order(self, id: str) -> bool:
        proto_order = order_event_pb2.Order()
        proto_order.id = id
        serialized_data = proto_order.SerializeToString()
        
        logging.info("Order serialized successfully.")
        
        return self._send_to_kafka(serialized_data, "delete")

    def _serialize_order(self, order: Order) -> bytes:
        proto_order = order_event_pb2.Order()
        proto_order.id = order.id
        proto_order.customer_id = order.customer_id
        proto_order.product_ids = order.product_ids
        proto_order.created_date = order.created_date
        proto_order.updated_date = order.updated_date
        return proto_order.SerializeToString()

    def _send_to_kafka(self, message: bytes, action: str) -> bool:
        try:
            self.kafka_client.produce_message(self.kafka_topic, message)
            logging.info(f"Order {action} message sent to Kafka successfully.")
            return True
        except Exception as e:
            logging.error(f"Failed to send order {action} message to Kafka: {e}")
            return False
