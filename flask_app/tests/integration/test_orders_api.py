import json
import logging
import time

base_url = "/api/v1/order/"


def validate_kafka_message(kafka_consumer, expected_order):
    from flask_app.app.utils.kafka.kafka_messages.serializers.proto_order_serializer import ProtoOrderSerializer
    from flask_app.app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import OperationType

    msg = None
    latest_msg = None
    while True:
        msg = kafka_consumer.poll(1.0)
        if msg is not None:
            latest_msg = ProtoOrderSerializer.deserialize_order(msg.value())
        else:
            break
    logging.info(
        f"[validate_kafka_message] Kafka consumed message: {str(OperationType.Name(latest_msg.operation_type))} - {latest_msg.proto_order}")

    assert expected_order['order']['id'] == latest_msg.proto_order.id
    assert expected_order['order']['customer_id'] == latest_msg.proto_order.customer_id
    assert expected_order['order']['product_ids'] == latest_msg.proto_order.product_ids


def test_create_order(client, kafka_consumer):
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
    validate_kafka_message(kafka_consumer, get_response)


def test_update_order(client, kafka_consumer):
    payload = {
        "customer_id": "customer_123",
        "product_ids": "product_1"
    }
    post_response = client.post(base_url, json=payload)
    post_response = post_response.get_json()

    update_payload = {
        "customer_id": "customer_123",
        "product_ids": "product_2"
    }

    logging.info("[test_create_order] Sending PUT request to update an order")
    put_response = client.put(f"{base_url}{post_response['order']['id']}", json=update_payload)

    logging.info("[test_create_order] Validate the response code")
    assert put_response.status_code == 200, "Failed to update order. Unexpected status code."
    put_response = put_response.get_json()

    logging.info("[test_create_order] Validate the order updated as expected. ")
    get_response = client.get(f"{base_url}{put_response['order']['id']}")
    get_response = get_response.get_json()

    assert get_response['order']['id'] == put_response['order']['id']
    assert get_response['order']['customer_id'] == put_response['order']['customer_id']
    assert get_response['order']['product_ids'] == put_response['order']['product_ids']
    # assert get_response['order']['created_date'] == put_response['order']['created_date']
    # assert get_response['order']['updated_date'] == put_response['order']['updated_date']
    validate_kafka_message(kafka_consumer, get_response)


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
