import time

import pytest
import logging
base_url = "/api/v1/order/"


def test_capital_case(client):
    # Define a payload for creating a new order
    payload = {
        "customer_id": "customer_123",
        "product_ids": "product_1"
    }

    # Send a POST request to create a new order
    logging.info("Sending POST request to create a new order")
    response = client.post(base_url, json=payload)
    # logging.info("**** response: " + response)
    logging.info("**** all looks ok, maybe its ok.")
