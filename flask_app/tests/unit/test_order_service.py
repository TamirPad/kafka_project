# # tests/unit/test_order_service.py
# import pytest
# from app.services.order_service import OrderService
# from app.dao.orders_dao import OrderDao, Order
# from app.utils.kafka.kafkaClient import KafkaClient

# @pytest.fixture
# def order_service():
#     # Use a mock KafkaClient and OrderDao for testing OrderService
#     mock_kafka_client = KafkaClient("localhost:9092")
#     mock_order_dao = OrderDao(db=None)  # Replace db with mock
#     return OrderService(mock_kafka_client, mock_order_dao)

# def test_create_order(order_service):
#     # Create a mock order for testing
#     mock_order = Order(id="123", customer_id="customer_123", product_ids="product_1", created_date="2024-06-09", updated_date="2024-06-09")

#     # Test creating an order
#     assert order_service.create_order(mock_order) is None  # Since create_order returns None

# def test_update_order(order_service):
#     # Create a mock order for testing
#     mock_order = Order(id="123", customer_id="customer_123", product_ids="product_1", created_date="2024-06-09", updated_date="2024-06-09")

#     # Test updating an order
#     assert order_service.update_order(mock_order) is None  # Since update_order returns None

# def test_delete_order(order_service):
#     # Create a mock order for testing
#     mock_order = Order(id="123", customer_id="customer_123", product_ids="product_1", created_date="2024-06-09", updated_date="2024-06-09")

#     # Test deleting an order
#     assert order_service.delete_order(mock_order) is None  # Since delete_order returns None
