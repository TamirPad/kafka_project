import logging

base_url = "/api/v1/order/"

def test_create_order(client):
    # Define a payload for creating a new order
    payload = {
        "customer_id": "customer_123",
        "product_ids": "product_1"
    }

    logging.info("[test_create_order] Sending POST request to create a new order")
    post_response = client.post(base_url, json=payload)

    logging.info("[test_create_order] Validate the response code")
    assert post_response.status_code == 201, "Failed to create order. Unexpected status code."
    post_response = post_response.get_json()

    logging.info("[test_create_order] Validate the order created as expected. ")
    get_response = client.get(f"{base_url}{post_response['order']['id']}")
    get_response = get_response.get_json()

    assert get_response['order']['id'] == post_response['order']['id']
    assert get_response['order']['customer_id'] == post_response['order']['customer_id']
    assert get_response['order']['product_ids'] == post_response['order']['product_ids']
    # assert get_response['order']['created_date'] == post_response['order']['created_date']
    # assert get_response['order']['updated_date'] == post_response['order']['updated_date']

    # validate kafaka message was produced by consuming it.


def test_get_order_order_not_found(client):
    # Send a GET request to retrieve an order by its ID
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    logging.info("Sending GET request to retrieve order with ID: %s", order_id)
    response = client.get(f"{base_url}{order_id}")

    # Validate the response
    assert response.status_code == 404, "Failed to retrieve order. Unexpected status code."


def test_update_order_order_not_found(client):
    # Define a payload for updating an existing order
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    payload = {
        "customer_id": "customer_456",
        "product_ids": "product_2"
    }

    # Send a PUT request to update the order
    logging.info("Sending PUT request to update order with ID: %s", order_id)
    response = client.put(f"{base_url}{order_id}", json=payload)

    assert response.status_code == 404, "Failed to update order. Unexpected status code."


def test_delete_order_order_not_found(client):
    # Define an order ID for deleting
    order_id = "894fc9e9-d316-4092-ba1d-4f4dc41e5371"
    
    # Send a DELETE request to delete the order
    logging.info("Sending DELETE request to delete order with ID: %s", order_id)
    response = client.delete(f"{base_url}{order_id}")

    assert response.status_code == 404, "Failed to delete order.Unexpected status code."





