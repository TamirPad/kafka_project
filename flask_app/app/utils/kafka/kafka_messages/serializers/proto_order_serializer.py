import logging
from app.dao.orders_dao import Order
from app.utils.kafka.kafka_messages.generated_protobuf import order_event_pb2

class ProtoOrderSerializer:
    
    @staticmethod
    def serialize_order(order: Order) -> bytes:
        try:
            logging.debug(f"Oder to serialize: {order.to_dict()}")
            proto_order = order_event_pb2.Order()
            proto_order.id = order.id
            proto_order.customer_id = order.customer_id
            proto_order.product_ids = order.product_ids
            proto_order.created_date = order.created_date
            proto_order.updated_date = order.updated_date

            serialized_order = proto_order.SerializeToString()
            logging.debug("Order serialized successfully.")
            return serialized_order
        except Exception as e:
            logging.error(f"Error serializing order: {e}")
            raise

    @staticmethod
    def deserialize_order(msg: bytes) -> order_event_pb2.Order:
        try:
            proto_order = order_event_pb2.Order()
            proto_order.ParseFromString(msg)
            logging.debug("Order deserialized successfully.")
            return proto_order
        except Exception as e:
            logging.error(f"Error deserializing order: {e}")
            raise
