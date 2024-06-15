import logging
from app.models.order import Order
from app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import ProtoOrder, OperationType, OrderMessage

class ProtoOrderSerializer:
    
    @staticmethod
    def serialize_order(order: Order, operation_type: OperationType) -> bytes:
        try:
            logging.debug(f"[ProtoOrderSerializer.serialize_order] Proto Order to serialize: {order.to_dict()}")
            proto_order =ProtoOrder()
            proto_order.id = order.id
            proto_order.customer_id = order.customer_id
            proto_order.product_ids = order.product_ids
            proto_order.created_date = order.created_date
            proto_order.updated_date = order.updated_date
            
            order_message = OrderMessage(
                operation_type = operation_type,
                proto_order = proto_order
            )

            serialized_order = order_message.SerializeToString()
            logging.debug("[ProtoOrderSerializer.serialize_order] Order serialized successfully.")
            return serialized_order
        except Exception as e:
            logging.error(f"Error serializing order: {e}")
            raise

    @staticmethod
    def deserialize_order(msg: bytes) -> OrderMessage:
        try:
            order_message = OrderMessage()
            order_message.ParseFromString(msg)
            logging.debug("Order deserialized successfully.")
            return order_message
        except Exception as e:
            logging.error(f"Error deserializing order: {e}")
            raise
