import unittest
from flask_app.app.api.v1.input_validator import InputValidator
from flask_app.tests.utlis.utils import generate_order_payload

class TestInputValidator(unittest.TestCase):

    def test_validate_create_order_input_success(self):
        payload = generate_order_payload()
        result, errors = InputValidator.validate_create_order_input(payload)
        self.assertTrue(result)
        self.assertEqual(errors, {})

    def test_validate_create_order_input_empty_payload(self):
        payload = {}
        result, errors = InputValidator.validate_create_order_input(payload)
        self.assertFalse(result)
        self.assertIn('customer_id', errors)
        self.assertIn('product_ids', errors)

    def test_validate_create_order_input_missing_customer_id(self):
        payload = generate_order_payload(customer_id=None)
        del payload['customer_id']
        result, errors = InputValidator.validate_create_order_input(payload)
        self.assertFalse(result)
        self.assertIn('customer_id', errors)
        self.assertNotIn('product_ids', errors)

    def test_validate_create_order_input_missing_product_ids(self):
        payload = generate_order_payload(product_ids=None)
        del payload['product_ids']
        result, errors = InputValidator.validate_create_order_input(payload)
        self.assertFalse(result)
        self.assertIn('product_ids', errors)
        self.assertNotIn('customer_id', errors)

    def test_validate_create_order_input_invalid_product_ids(self):
        payload = generate_order_payload(product_ids='p1')
        result, errors = InputValidator.validate_create_order_input(payload)
        self.assertFalse(result)
        self.assertIn('product_ids', errors)

    def test_validate_update_order_input_success(self):
        payload = generate_order_payload()
        result, errors = InputValidator.validate_update_order_input(payload)
        self.assertTrue(result)
        self.assertEqual(errors, {})

    def test_validate_update_order_input_empty_payload(self):
        payload = {}
        result, errors = InputValidator.validate_update_order_input(payload)
        self.assertFalse(result)
        self.assertIn('payload', errors)

    def test_validate_update_order_input_invalid_customer_id(self):
        payload = generate_order_payload()
        payload['customer_id'] = 123  # invalid customer_id
        result, errors = InputValidator.validate_update_order_input(payload)
        self.assertFalse(result)
        self.assertIn('customer_id', errors)

    def test_validate_update_order_input_invalid_product_ids(self):
        payload = generate_order_payload(product_ids='p1')
        result, errors = InputValidator.validate_update_order_input(payload)
        self.assertFalse(result)
        self.assertIn('product_ids', errors)

    def test_validate_order_id_success(self):
        order_id = 'order123'
        result, errors = InputValidator.validate_order_id(order_id)
        self.assertTrue(result)
        self.assertEqual(errors, {})

    def test_validate_order_id_empty(self):
        order_id = ''
        result, errors = InputValidator.validate_order_id(order_id)
        self.assertFalse(result)
        self.assertIn('order_id', errors)


if __name__ == '__main__':
    unittest.main()
