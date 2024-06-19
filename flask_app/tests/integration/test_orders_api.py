import json
import logging
import uuid

base_url = "/api/v1/order/"


def validate_kafka_message(kafka_message_holder, event_type, expected_order):
    from flask_app.app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import OperationType

    order_id_kafka_messages = kafka_message_holder.get_messages_by_order_id(expected_order['id'])
    for msg in order_id_kafka_messages:
        if str(OperationType.Name(msg.operation_type)) == event_type:
            if expected_order['customer_id'] == msg.proto_order.customer_id and expected_order['product_ids'] == msg.proto_order.product_ids:
                assert expected_order['id'] == msg.proto_order.id
                assert expected_order['customer_id'] == msg.proto_order.customer_id
                assert expected_order['product_ids'] == msg.proto_order.product_ids


def create_order(client, payload):
    logging.info("Sending POST request to create a new order")
    response = client.post(base_url, json=payload)
    assert response.status_code == 201, "Failed to create order. Unexpected status code."
    response_data = response.get_json().get('data')
    assert response_data is not None, "Response data does not contain 'data' key"
    return response_data.get('order')


def retrieve_order(client, order_id):
    logging.info("Sending GET request to retrieve order with ID: %s", order_id)
    response = client.get(f"{base_url}{order_id}")
    assert response.status_code == 200, "Failed to retrieve order. Unexpected status code."
    response_data = response.get_json().get('data')
    assert response_data is not None, "Response data does not contain 'data' key"
    return response_data.get('order')


def update_order(client, order_id, payload):
    logging.info("Sending PUT request to update order with ID: %s", order_id)
    response = client.put(f"{base_url}{order_id}", json=payload)
    assert response.status_code == 200, "Failed to update order. Unexpected status code."
    response_data = response.get_json().get('data')
    assert response_data is not None, "Response data does not contain 'data' key"
    return response_data.get('order')


def delete_order(client, order_id):
    logging.info("Sending DELETE request to delete order with ID: %s", order_id)
    response = client.delete(f"{base_url}{order_id}")
    assert response.status_code == 204, "Failed to delete order. Unexpected status code."


def generate_order_payload(customer_id=None, product_ids=None):
    if product_ids is None:
        product_ids = [f"product_{uuid.uuid4()}"]
    elif not isinstance(product_ids, list):
        product_ids = [product_ids]

    return {
        "customer_id": customer_id or f"customer_{uuid.uuid4()}",
        "product_ids": product_ids
    }


def test_create_order(client, kafka_message_holder):
    payload = generate_order_payload()

    created_order = create_order(client, payload)
    retrieved_order = retrieve_order(client, created_order['id'])

    assert retrieved_order['id'] == created_order['id'], "Retrieved order ID does not match created order ID"
    assert retrieved_order['customer_id'] == created_order['customer_id'], "Customer IDs do not match"
    assert json.loads(retrieved_order['product_ids']) == created_order['product_ids'], "Product IDs do not match"

    validate_kafka_message(kafka_message_holder, "ORDER_CREATED", retrieve_order(client, created_order['id']))


def test_update_order(client, kafka_message_holder):
    create_payload = generate_order_payload()

    created_order = create_order(client, create_payload)

    update_payload = generate_order_payload(customer_id=created_order['customer_id'])

    updated_order = update_order(client, created_order['id'], update_payload)
    retrieved_order = retrieve_order(client, updated_order['id'])

    assert retrieved_order['id'] == updated_order['id'], "Retrieved order ID does not match updated order ID"
    assert retrieved_order['customer_id'] == updated_order['customer_id'], "Customer IDs do not match"
    assert json.loads(retrieved_order['product_ids']) == updated_order['product_ids'], "Product IDs do not match"

    validate_kafka_message(kafka_message_holder, "ORDER_UPDATED", retrieve_order(client, updated_order['id']))


def test_create_and_update_order_twice(client, kafka_message_holder):
    # Create an order
    create_payload = generate_order_payload()
    created_order = create_order(client, create_payload)

    # First update
    first_update_payload = generate_order_payload(customer_id=created_order['customer_id'])
    first_updated_order = update_order(client, created_order['id'], first_update_payload)

    # Validate first update
    first_retrieved_order = retrieve_order(client, first_updated_order['id'])
    assert first_retrieved_order['id'] == first_updated_order['id'], "First retrieved order ID does not match updated order ID"
    assert first_retrieved_order['customer_id'] == first_updated_order['customer_id'], "First customer IDs do not match"
    assert json.loads(first_retrieved_order['product_ids']) == first_updated_order['product_ids'], "First product IDs do not match"

    # Second update
    second_update_payload = generate_order_payload(customer_id=created_order['customer_id'])
    second_updated_order = update_order(client, created_order['id'], second_update_payload)

    # Validate second update
    second_retrieved_order = retrieve_order(client, second_updated_order['id'])
    assert second_retrieved_order['id'] == second_updated_order['id'], "Second retrieved order ID does not match updated order ID"
    assert second_retrieved_order['customer_id'] == second_updated_order['customer_id'], "Second customer IDs do not match"
    assert json.loads(second_retrieved_order['product_ids']) == second_updated_order['product_ids'], "Second product IDs do not match"

    # Validate Kafka message for the second update
    validate_kafka_message(kafka_message_holder, "ORDER_UPDATED", retrieve_order(client, second_updated_order['id']))


def test_delete_order(client, kafka_message_holder):
    # Create an order to delete
    create_payload = generate_order_payload()
    created_order = create_order(client, create_payload)

    # Delete the order
    delete_order(client, created_order['id'])

    # Attempt to retrieve the deleted order and validate it returns 404
    logging.info("Sending GET request to retrieve deleted order with ID: %s", created_order['id'])
    response = client.get(f"{base_url}{created_order['id']}")
    assert response.status_code == 404, "Deleted order was still retrievable. Unexpected status code."


def test_get_order_order_not_found(client):
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    logging.info("Sending GET request to retrieve order with ID: %s", order_id)
    response = client.get(f"{base_url}{order_id}")

    assert response.status_code == 404, "Failed to retrieve order. Unexpected status code."


def test_update_order_order_not_found(client):
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    payload = generate_order_payload()

    logging.info("Sending PUT request to update order with ID: %s", order_id)
    response = client.put(f"{base_url}{order_id}", json=payload)
    assert response.status_code == 404, "Failed to update order. Unexpected status code."


def test_delete_order_order_not_found(client):
    order_id = "894fc9e9-d316-4092-ba1d-4f4dc41e5371"
    logging.info("Sending DELETE request to delete order with ID: %s", order_id)
    response = client.delete(f"{base_url}{order_id}")
    assert response.status_code == 404, "Failed to delete order. Unexpected status code."
