# tests/unit/test_orders_dao.py
import pytest
from app.dao.orders_dao import OrderDao, Order
from app.utils.sql.db import MySQLClient

@pytest.fixture
def order_dao():
    # Use a mock MySQLClient for testing OrderDao
    mock_db = MySQLClient(host="localhost", user="test_user", password="test_password", database="test_db", port=3306)
    return OrderDao(mock_db)

def test_create_order(order_dao):
    # Create a mock order for testing
    mock_order = Order(id="123", customer_id="customer_123", product_ids="product_1", created_date="2024-06-09", updated_date="2024-06-09")

    # Test creating an orderclear
    new_order = order_dao.create_order(mock_order)
    assert new_order.id == mock_order.id

    # Test getting the created order
    retrieved_order = order_dao.get_order(new_order.id)
    assert retrieved_order.id == new_order.id

def test_get_order(order_dao):
    # Test retrieving an existing order
    existing_order_id = "123"
    retrieved_order = order_dao.get_order(existing_order_id)
    assert retrieved_order.id == existing_order_id

    # Test retrieving a non-existing order
    non_existing_order_id = "456"
    assert order_dao.get_order(non_existing_order_id) is None
