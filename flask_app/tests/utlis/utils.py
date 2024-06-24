import uuid


def generate_order_payload(customer_id=None, product_ids=None):
    if product_ids is None:
        product_ids = [f"product_{uuid.uuid4()}"]
    elif not isinstance(product_ids, list):
        product_ids = [product_ids]

    return {
        "customer_id": customer_id or f"customer_{uuid.uuid4()}",
        "product_ids": product_ids
    }
