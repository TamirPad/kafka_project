import pytest
from app.utils.sql.db import init_db
from app.dao.orders_dao import OrderDao, Order

@pytest.fixture(scope="module")
def database():
    # Setup: Initialize the database
    db = init_db()
    yield db  # Pass the initialized database client to the tests
    # Teardown: Clean up any resources if needed

def test_create_order(database):
    # Test creating a new order in the database
    order_dao = OrderDao(database)
    new_order = Order(id="123", customer_id="customer_123", product_ids="product_1", created_date="2024-06-05 04:26:27", updated_date="2024-06-05 04:26:27")
    
    # Perform the database operation
    created = order_dao.create_order(new_order)
    
    # Assert the result
    assert type(created) == Order

def test_get_order(database):
    # Test retrieving an order from the database by its ID
    order_dao = OrderDao(database)
    existing_order_id = "123"
    
    # Perform the database operation
    retrieved_order = order_dao.get_order(existing_order_id)
    
    # Assert the result
    assert retrieved_order is not None
    assert retrieved_order.id == existing_order_id

def test_update_order(database):
    # Test updating an existing order in the database
    order_dao = OrderDao(database)
    existing_order_id = "123"
    updated_order = Order(id=existing_order_id, customer_id="customer_456", product_ids="product_2", created_date="2024-06-05 04:26:27", updated_date="2024-06-05 04:26:27")
    
    # Perform the database operation
    updated = order_dao.update_order(updated_order)
    
    # Assert the result
    assert type(updated) == Order

def test_delete_order(database):
    # Test deleting an order from the database by its ID
    order_dao = OrderDao(database)
    existing_order_id = "123"
    order_to_delete = Order(id=existing_order_id, customer_id="customer_456", product_ids="product_2", created_date="2024-06-05 04:26:27", updated_date="2024-06-05 04:26:27")

    
    # Perform the database operation
    deleted = order_dao.delete_order(order_to_delete)
    
    # Assert the result
    assert type(deleted) == Order
