import logging
from datetime import datetime
from typing import Tuple, Optional
import json
import uuid
from flask import render_template, Blueprint, jsonify, request
from app.dao.orders_dao import OrderDao, Order
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
def handle_error(e):
    """
    Global error handler for the orders API.

    Args:
        e (Exception): The exception that occurred.

    Returns:
        Tuple[dict, int]: A tuple containing the error response JSON and HTTP status code.
    """
    logging.error('[orders_api.handle_error] An error occurred: %s', e)
    return jsonify({"error": "Internal Server Error"}), 500


@orders_bp.route('/')
def index() -> str:
    """
    Display index page with a list of all orders.

    Returns:
        str: Rendered HTML template.
    """
    try:
        
        orders = order_dao.get_all_orders()
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
    return render_template('index.html', orders=orders)


@orders_bp.route('/api/v1/order/', methods=['POST'])
def create_order() -> Tuple[dict, int]:
    """
    Create a new order.

    Returns:
        Tuple[dict, int]: A tuple containing the response JSON and HTTP status code.
    """
    payload = request.get_json()

    if not payload or 'customer_id' not in payload or 'product_ids' not in payload:
        return jsonify({"error": "Missing required fields: customer_id, product_ids"}), 400
    
    try:
        new_order = Order(str(uuid.uuid4()), payload.get('customer_id'), payload.get('product_ids'), datetime.now(), datetime.now())
        order_service.create_order(new_order)
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Order created", "order_id": new_order.id}), 201


@orders_bp.route('/api/v1/order/<string:id>', methods=['GET'])
def get_order(id: str) -> Tuple[Optional[dict], int]:
    """
    Retrieve an order by its ID.

    Args:
        id (str): The ID of the order to retrieve.

    Returns:
        Tuple[Optional[dict], int]: A tuple containing the response JSON and HTTP status code.
    """
    if not id:
        return jsonify({"error": "Invalid order ID format"}), 400

    try:
        order = order_dao.get_order(id)
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

    if order:
        return  jsonify(order.to_dict()), 200

    return jsonify({"message": "Order not found"}), 404


@orders_bp.route('/api/v1/order/<string:id>', methods=['PUT'])
def update_order(id: str) -> Tuple[dict, int]:
    """
    Update an existing order.

    Args:
        id (str): The ID of the order to update.

    Returns:
        Tuple[dict, int]: A tuple containing the response JSON and HTTP status code.
    """
    payload = request.get_json()

    if not payload or 'customer_id' not in payload or 'product_ids' not in payload:
        return jsonify({"error": "Missing required fields: customer_id, product_ids"}), 400

    try:
        current_order = order_dao.get_order(id)
        if current_order == None:
            return jsonify({"message": "Order not found"}), 404
        else:
            updated_order = Order(id, payload.get('customer_id'), payload.get('product_ids'), current_order.created_date, datetime.now() )
            order_service.update_order(updated_order)
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Order updated", "order_id": id}), 200


@orders_bp.route('/api/v1/order/<string:id>', methods=['DELETE'])
def delete_order(id: str) -> Tuple[dict, int]:
    """
    Delete an order by its ID.

    Args:
        id (str): The ID of the order to delete.

    Returns:
        Tuple[dict, int]: A tuple containing the response JSON and HTTP status code.
    """
    if not id:
        return jsonify({"error": "Invalid order ID format"}), 400

    try:
        order_to_delete = order_dao.get_order(id)
        if order_to_delete == None:
            return jsonify({"message": "Order not found"}), 404
        else:
            order_service.delete_order(order_to_delete)
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Order deleted", "order_id": id}), 200
