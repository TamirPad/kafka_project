# import pytest
# from app.dao.orders_dao import Order
# from app.utils.kafka.kafka_messages.serializers.proto_order_serializer import ProtoOrderSerializer
# from app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import ProtoOrder, OperationType, OrderMessage

# @pytest.fixture
# def mock_order():
#     return Order(
#         id="123",
#         customer_id="customer_123",
#         product_ids="product_1",
#         created_date="2024-06-08",
#         updated_date="2024-06-08"
#     )

# def test_serialize_order(mock_order):
#     serialized_order = ProtoOrderSerializer.serialize_order(mock_order, OperationType.ORDER_CREATED)
#     assert isinstance(serialized_order, bytes)
#     # Add more assertions as needed to validate the serialized order

# def test_deserialize_order(mock_order):
#     proto_order = ProtoOrder()
#     proto_order.id = mock_order.id
#     proto_order.customer_id = mock_order.customer_id
#     proto_order.product_ids = mock_order.product_ids
#     proto_order.created_date = mock_order.created_date
#     proto_order.updated_date = mock_order.updated_date

#     order_message = OrderMessage(operation_type=OperationType.ORDER_CREATED, proto_order=proto_order)
#     serialized_order = order_message.SerializeToString()

#     deserialized_order_message = ProtoOrderSerializer.deserialize_order(serialized_order)
#     assert isinstance(deserialized_order_message, OrderMessage)
#     # Add more assertions as needed to validate the deserialized order message
