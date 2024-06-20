import json
import logging
import uuid

base_url = "/api/v1/order/"


def test_create_order(app_client, kafka_message_holder):
    payload = app_client.generate_order_payload()

    created_order = app_client.create_order(payload)
    assert created_order.status_code == 201, "Unexpected status code."
    created_order = created_order.get_json().get('data').get('order')

    retrieved_order = app_client.retrieve_order(created_order['id'])
    assert retrieved_order.status_code == 200, "Unexpected status code."
    retrieved_order = retrieved_order.get_json().get('data').get('order')

    assert retrieved_order['id'] == created_order['id'], "Retrieved order ID does not match created order ID"
    assert retrieved_order['customer_id'] == created_order['customer_id'], "Customer IDs do not match"
    assert json.loads(retrieved_order['product_ids']) == created_order['product_ids'], "Product IDs do not match"

    created_order_messages = kafka_message_holder.get_created_order_messages()
    for msg in created_order_messages:
        if retrieved_order['customer_id'] == msg.order_created.order.customer_id and json.loads(retrieved_order['product_ids']) == msg.order_created.order.product_ids:
            assert retrieved_order['id'] == msg.order_created.order.id
            assert retrieved_order['customer_id'] == msg.order_created.order.customer_id
            assert retrieved_order['product_ids'] == msg.order_created.order.product_ids


def test_get_order(app_client):
    payload = app_client.generate_order_payload()

    created_order = app_client.create_order(payload)
    assert created_order.status_code == 201, "Unexpected status code."
    created_order = created_order.get_json().get('data').get('order')

    retrieved_order = app_client.retrieve_order(created_order['id'])
    assert retrieved_order.status_code == 200, "Unexpected status code."
    retrieved_order = retrieved_order.get_json().get('data').get('order')

    assert retrieved_order['id'] == created_order['id'], "Retrieved order ID does not match created order ID"
    assert retrieved_order['customer_id'] == created_order['customer_id'], "Customer IDs do not match"
    assert json.loads(retrieved_order['product_ids']) == created_order['product_ids'], "Product IDs do not match"


def test_update_order(app_client, kafka_message_holder):
    create_payload = app_client.generate_order_payload()
    created_order = app_client.create_order(create_payload)
    assert created_order.status_code == 201, "Unexpected status code."
    created_order = created_order.get_json().get('data').get('order')

    update_payload = app_client.generate_order_payload(customer_id=created_order['customer_id'])
    updated_order = app_client.update_order(created_order['id'], update_payload)
    assert updated_order.status_code == 200, "Unexpected status code."
    updated_order = updated_order.get_json().get('data').get('order')

    retrieved_order = app_client.retrieve_order(updated_order['id'])
    assert retrieved_order.status_code == 200, "Unexpected status code."
    retrieved_order = retrieved_order.get_json().get('data').get('order')

    assert retrieved_order['id'] == updated_order['id'], "Retrieved order ID does not match updated order ID"
    assert retrieved_order['customer_id'] == updated_order['customer_id'], "Customer IDs do not match"
    assert json.loads(retrieved_order['product_ids']) == updated_order['product_ids'], "Product IDs do not match"

    updated_order_messages = kafka_message_holder.get_updated_order_messages()
    logging.debug("[test_orders_api] Validating kafka msg")
    for msg in updated_order_messages:
        if retrieved_order['customer_id'] == msg.order_updated.order.customer_id and json.loads(retrieved_order['product_ids']) == msg.order_updated.order.product_ids:
            assert retrieved_order['id'] == msg.order_updated.order.id
            assert retrieved_order['customer_id'] == msg.order_updated.order.customer_id
            assert json.loads(retrieved_order['product_ids']) == msg.order_updated.order.product_ids


def test_delete_order(app_client, kafka_message_holder):
    # Create an order to delete
    create_payload = app_client.generate_order_payload()
    created_order = app_client.create_order(create_payload)
    assert created_order.status_code == 201, "Unexpected status code."
    created_order = created_order.get_json().get('data').get('order')

    # Delete the order
    response = app_client.delete_order(created_order['id'])
    assert response.status_code == 204, "Unexpected status code."

    # Attempt to retrieve the deleted order and validate it returns 404
    response = app_client.retrieve_order(created_order['id'])
    assert response.status_code == 404, "Deleted order was still retrievable. Unexpected status code."

    deleted_order_messages = kafka_message_holder.get_deleted_order_messages()
    for msg in deleted_order_messages:
        assert created_order['id'] == msg.order_deleted.order_id


def test_get_order_order_not_found(app_client):
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    response = app_client.retrieve_order(order_id)

    assert response.status_code == 404, "Failed to retrieve order. Unexpected status code."


def test_update_order_order_not_found(app_client):
    order_id = "971b5ec2-b38f-4372-91f9-5d29a4854b8a"
    payload = app_client.generate_order_payload()

    response = app_client.update_order(order_id, payload)
    assert response.status_code == 404, "Failed to update order. Unexpected status code."


def test_delete_order_order_not_found(app_client):
    order_id = "894fc9e9-d316-4092-ba1d-4f4dc41e5371"
    response = app_client.delete_order(order_id)
    assert response.status_code == 404, "Failed to delete order. Unexpected status code."
