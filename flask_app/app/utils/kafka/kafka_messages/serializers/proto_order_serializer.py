import logging
from flask_app.app.models.order import Order as AppOrder
from flask_app.app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import Order, \
    OrderMessage, OrderCreated, OrderUpdated, OrderDeleted


class ProtoOrderSerializer:

    @staticmethod
    def create_proto_order(order: AppOrder) -> Order:
        return Order(
            id=order.id,
            customer_id=order.customer_id,
            product_ids=order.product_ids,
            created_date=order.created_date,
            updated_date=order.updated_date
        )

    @staticmethod
    def _serialize_create(order: AppOrder) -> OrderMessage:
        proto_order = ProtoOrderSerializer.create_proto_order(order)
        order_created = OrderCreated()
        order_created.order.CopyFrom(proto_order)
        order_message = OrderMessage()
        order_message.order_created.CopyFrom(order_created)
        return order_message

    @staticmethod
    def _serialize_update(order: AppOrder) -> OrderMessage:
        proto_order = ProtoOrderSerializer.create_proto_order(order)
        order_updated = OrderUpdated()
        order_updated.order.CopyFrom(proto_order)
        order_message = OrderMessage()
        order_message.order_updated.CopyFrom(order_updated)
        return order_message

    @staticmethod
    def _serialize_delete(order: AppOrder) -> OrderMessage:
        order_deleted = OrderDeleted(order_id=order.id)
        order_message = OrderMessage()
        order_message.order_deleted.CopyFrom(order_deleted)
        return order_message

    @staticmethod
    def serialize_order(order: AppOrder, operation: str) -> bytes:
        try:
            logging.debug(f"[ProtoOrderSerializer.serialize_order] Order to serialize: {order.to_dict()}")

            operation_function_mapping = {
                "create": ProtoOrderSerializer._serialize_create,
                "update": ProtoOrderSerializer._serialize_update,
                "delete": ProtoOrderSerializer._serialize_delete
            }

            # Get the appropriate function based on the operation
            operation_function = operation_function_mapping.get(operation)
            order_message = operation_function(order)

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
