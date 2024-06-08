import logging

base_url = "/api/v1/order/"

def test_create_order(client):
    logging.info(f"{'*'*50}test_create_order{'*'*50}")
    # Define a payload for creating a new order
    payload = {
        "customer_id": "customer_123",
        "product_ids": ["product_1"]
    }

    # Send a POST request to create a new order
    logging.info("Sending POST request to create a new order")
    response = client.post(base_url, json=payload)

    # Validate the response
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["message"] == "Order created"

def test_get_order(client):
    logging.info(f"{'*'*50}test_get_order{'*'*50}")

    # Send a GET request to retrieve an order by its ID
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    logging.info("Sending GET request to retrieve order with ID: %s", order_id)
    response = client.get(f"{base_url}{order_id}")

    # Validate the response
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["id"] == order_id

def test_update_order(client):
    logging.info(f"{'*'*50}test_update_order{'*'*50}")

    # Define a payload for updating an existing order
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    payload = {
        "customer_id": "customer_456",
        "product_ids": ["product_2"]
    }

    # Send a PUT request to update the order
    logging.info("Sending PUT request to update order with ID: %s", order_id)
    response = client.put(f"{base_url}{order_id}", json=payload)

    # Validate the response
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Order updated"
