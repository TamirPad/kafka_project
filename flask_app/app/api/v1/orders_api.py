import logging
from datetime import datetime
from typing import Tuple, Optional
import uuid
from flask import render_template, Blueprint, jsonify, request, Response
from app.dao.orders_dao import OrderDao
from app.models.order import Order
from app.config import Config
from app.services.order_service import OrderService
from app.utils.kafka.kafkaClient import KafkaClient
from app.utils.sql.db import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

orders_bp = Blueprint('orders', __name__)

kafka_client = KafkaClient(Config.KAFKA_BOOTSTRAP_SERVERS)
order_dao = OrderDao(db)
order_service = OrderService(kafka_client, order_dao)


@orders_bp.errorhandler(Exception)
def handle_error(e) -> tuple[Response, int]:
    """
    Handle unexpected errors by logging the error and returning a generic error response.

    Args:
        e (Exception): The exception that was raised.

    Returns:
        tuple[Response, int]: A tuple containing a JSON response with an error message and the HTTP status code 500.
    """
    logging.error('[orders_api.handle_error] An error occurred: %s', e)
    return jsonify({"error": "Internal Server Error"}), 500


@orders_bp.route('/')
def index() -> tuple[Response, int] | str:
    """
    Render the index page with a list of all orders.

    Returns:
        tuple[Response, int] | str: The rendered template or an error response.
    """
    try:
        orders = order_dao.get_all_orders()
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
    return render_template('index.html', orders=orders)


@orders_bp.route('/api/v1/order/', methods=['POST'])
def create_order() -> tuple[Response, int]:
    """
    Create a new order based on the provided payload.

    Returns:
        tuple[Response, int]: A tuple containing a JSON response with a success message and the HTTP status code 201 or an error message and the appropriate status code.
    """
    payload = request.get_json()

    if not payload or 'customer_id' not in payload or 'product_ids' not in payload:
        return jsonify({"error": "Missing required fields: customer_id, product_ids"}), 400

    try:
        new_order = Order(str(uuid.uuid4()), payload.get('customer_id'), payload.get('product_ids'), datetime.now(), datetime.now())
        order_service.create_order(new_order)
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Order created", "order": new_order.to_dict()}), 201


@orders_bp.route('/api/v1/order/<string:id>', methods=['GET'])
def get_order(id: str) -> tuple[Response, int]:
    """
    Retrieve an order by its ID.

    Args:
        id (str): The ID of the order.

    Returns:
        tuple[Response, int]: A tuple containing a JSON response with the order details and the HTTP status code 200 or an error message and the appropriate status code.
    """
    if not id:
        return jsonify({"error": "Invalid order ID format"}), 400

    try:
        order = order_dao.get_order(id)
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

    if order:
        return jsonify({"message": "Order received", "order": order.to_dict()}), 200
    else:
        return jsonify({"message": "Order not found"}), 404


@orders_bp.route('/api/v1/order/<string:id>', methods=['PUT'])
def update_order(id: str) -> tuple[Response, int]:
    """
    Update an existing order based on the provided payload.

    Args:
        id (str): The ID of the order.

    Returns:
        tuple[Response, int]: A tuple containing a JSON response with a success message and the HTTP status code 200 or an error message and the appropriate status code.
    """
    payload = request.get_json()

    if not payload or 'customer_id' not in payload or 'product_ids' not in payload:
        return jsonify({"error": "Missing required fields: customer_id, product_ids"}), 400

    try:
        updated_order = Order(id, payload.get('customer_id'), payload.get('product_ids'), 'created_time', datetime.now())
        updated = order_service.update_order(updated_order)
        if not updated:
            return jsonify({"message": "Order not found"}), 404
        else:
            return jsonify({"message": "Order updated", "order": updated_order.to_dict()}), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@orders_bp.route('/api/v1/order/<string:id>', methods=['DELETE'])
def delete_order(id: str) -> tuple[Response, int]:
    """
    Delete an order by its ID.

    Args:
        id (str): The ID of the order.

    Returns:
        tuple[Response, int]: A tuple containing a JSON response with a success message and the HTTP status code 200 or an error message and the appropriate status code.
    """
    if not id:
        return jsonify({"error": "Invalid order ID format"}), 400

    try:
        deleted = order_service.delete_order(Order(id, '', '', '', ''))
        if not deleted:
            return jsonify({"message": "Order not found"}), 404
        else:
            return jsonify({"message": "Order deleted", "order": deleted.to_dict()}), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
