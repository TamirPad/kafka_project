import logging
from flask_app.app.models.order import Order as AppOrder
from flask_app.app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import Order, \
    OrderMessage, OrderCreated, OrderUpdated, OrderDeleted


class ProtoOrderSerializer:

    @staticmethod
    def serialize_order(order: AppOrder, operation: str) -> bytes:
        try:
            logging.debug(f"[ProtoOrderSerializer.serialize_order] Order to serialize: {order.to_dict()}")

            # Create the protobuf Order message from the AppOrder
            proto_order = Order(
                id=order.id,
                customer_id=order.customer_id,
                product_ids=order.product_ids,
                created_date=order.created_date,
                updated_date=order.updated_date
            )

            # Create the OrderMessage and set the appropriate oneof field
            order_message = OrderMessage()

            if operation == "create":
                order_created = OrderCreated()
                order_created.order.CopyFrom(proto_order)
                order_message.order_created.CopyFrom(order_created)
            elif operation == "update":
                order_updated = OrderUpdated()
                order_updated.order.CopyFrom(proto_order)
                order_message.order_updated.CopyFrom(order_updated)
            elif operation == "delete":
                order_deleted = OrderDeleted(order_id=order.id)
                order_message.order_deleted.CopyFrom(order_deleted)
            else:
                raise ValueError(f"Unsupported operation type: {operation}")

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
