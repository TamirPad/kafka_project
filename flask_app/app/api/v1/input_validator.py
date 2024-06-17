from typing import Dict, Any, Tuple

class InputValidator:
    @staticmethod
    def validate_create_order_input(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        errors = {}
        if not payload:
            errors["payload"] = "Payload is required."
        if 'customer_id' not in payload:
            errors["customer_id"] = "Customer ID is required."
        if 'product_ids' not in payload:
            errors["product_ids"] = "Product IDs are required."
        elif not isinstance(payload['product_ids'], str):
            errors["product_ids"] = "Product IDs should be a string."

        if errors:
            return False, errors
        return True, {}

    @staticmethod
    def validate_update_order_input(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        errors = {}
        if not payload:
            errors["payload"] = "Payload is required."
        if 'customer_id' in payload and not isinstance(payload['customer_id'], str):
            errors["customer_id"] = "Customer ID must be a string."
        if 'product_ids' in payload and not isinstance(payload['product_ids'], str):
            errors["product_ids"] = "Product IDs should be a string."

        if errors:
            return False, errors
        return True, {}

    @staticmethod
    def validate_order_id(order_id: str) -> Tuple[bool, Dict[str, Any]]:
        if not order_id:
            return False, {"order_id": "Order ID is required."}
        return True, {}
