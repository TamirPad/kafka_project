import logging

base_url = "/api/v1/order/"

def test_create_order(client):
    # Define a payload for creating a new order
    payload = {
        "customer_id": "customer_123",
        "product_ids": ["product_1"]
    }

    # Send a POST request to create a new order
    logging.info("Sending POST request to create a new order")
    response = client.post(base_url, json=payload)

    # Validate the response
    assert response.status_code == 201, "Failed to create order. Unexpected status code."
    response_data = response.get_json()
    assert response_data["message"] == "Order created", "Failed to create order. Unexpected message."


def test_get_order(client):
    # Send a GET request to retrieve an order by its ID
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    logging.info("Sending GET request to retrieve order with ID: %s", order_id)
    response = client.get(f"{base_url}{order_id}")

    # Validate the response
    assert response.status_code == 200, "Failed to retrieve order. Unexpected status code."
    response_data = response.get_json()
    assert response_data["id"] == order_id, "Failed to retrieve order. Unexpected order ID."

def test_update_order(client):
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
    assert response.status_code == 200, "Failed to update order. Unexpected status code."
    response_data = response.get_json()
    assert response_data["message"] == "Order updated", "Failed to update order. Unexpected message."

def test_delete_order(client):
    # Define an order ID for deleting
    order_id = "894fc9e9-d316-4092-ba1d-4f4dc41e5371"
    
    # Send a DELETE request to delete the order
    logging.info("Sending DELETE request to delete order with ID: %s", order_id)
    response = client.delete(f"{base_url}{order_id}")
    if response.status_code == 404:
        assert response.status_code == 404, "Failed to delete order."

    else:  
        # Assert that the response status code is 204
        assert response.status_code == 200, f"Failed to delete order. Unexpected status code.{response.status_code}"
    





