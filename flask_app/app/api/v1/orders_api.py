import json
import logging
from datetime import datetime
from typing import Tuple, Optional
import uuid
from app.api.v1.input_validator import InputValidator
from flask import render_template, Blueprint, jsonify, request, Response
from app.dao.orders_dao import OrderDao
from app.models.order import Order
from app.config import Config
from app.services.order_service import OrderService
from app.utils.kafka.kafkaClient import KafkaClient
from app.utils.sql.db import mysql_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

orders_bp = Blueprint('orders', __name__)

kafka_client = KafkaClient(Config.KAFKA_BOOTSTRAP_SERVERS)
order_dao = OrderDao(mysql_client)
order_service = OrderService(kafka_client, order_dao)


@orders_bp.errorhandler(Exception)
def handle_error(e) -> Response:
    """
    Handle unexpected errors by logging the error and returning a generic error response.

    Args:
        e (Exception): The exception that was raised.

    Returns:
        Response: A JSON response with an error message and the HTTP status code 500.
    """
    logging.error('[orders_api.handle_error] An error occurred: %s', e)
    # return jsonify({"error": "Internal Server Error"}), 500
    return Response(response=json.dumps({"data": {"error": "Internal Server Error"}}), status=500)


@orders_bp.route('/')
def index() -> Response | str:
    """
    Render the index page with a list of all orders.

    Returns:
        Response | str: The rendered template or an error response.
    """
    try:
        orders = order_dao.get_all_orders()
    except Exception:
        return Response(response=json.dumps({"data": {"error": "Internal Server Error"}}), status=500)
    return render_template('index.html', orders=orders)


@orders_bp.route('/api/v1/order/', methods=['POST'])
def create_order() -> Response:
    """
    Create a new order based on the provided payload.

    Returns:
        Response: A JSON response with a success message and the HTTP status code 201 or an error message and the appropriate status code.
    """
    payload = request.get_json()
    is_valid, errors = InputValidator.validate_create_order_input(payload)

    if not is_valid:
        return Response(response=json.dumps({"data": {"error": "Invalid input", "errors": errors}}),
                        status=400, mimetype='application/json')

    try:
        new_order = Order(str(uuid.uuid4()), payload.get('customer_id'), payload.get('product_ids'), datetime.now(),
                          datetime.now())
        order_service.create_order(new_order)
        return Response(response=json.dumps({"data": {"message": "Order created", "order": new_order.to_dict()}}),
                        status=201, mimetype='application/json')

    except Exception:
        return Response(response=json.dumps({"data": {"error": "Internal Server Error"}}), status=500,
                        mimetype='application/json')


@orders_bp.route('/api/v1/order/<string:id>', methods=['GET'])
def get_order(id: str) -> Response:
    """
    Retrieve an order by its ID.

    Args:
        id (str): The ID of the order.

    Returns:
        Response: A JSON response with the order details and the HTTP status code 200 or an error message and the appropriate status code.
    """
    is_valid, errors = InputValidator.validate_order_id(id)
    if not is_valid:
        return Response(response=json.dumps({"data": {"error": "Invalid input", "errors": errors}}),
                        status=400, mimetype='application/json')

    try:
        order = order_dao.get_order(id)
    except Exception:
        return Response(response=json.dumps({"data": {"error": "Internal Server Error"}}), status=500,
                        mimetype='application/json')

    if order:
        return Response(response=json.dumps({"data": {"message": "Order received", "order": order.to_dict()}}),
                        status=200, mimetype='application/json')
    else:
        return Response(response=json.dumps({"data": {"message": "Order not found"}}), status=404,
                        mimetype='application/json')


@orders_bp.route('/api/v1/order/<string:id>', methods=['PUT'])
def update_order(id: str) -> Response:
    """
    Update an existing order based on the provided payload.

    Args:
        id (str): The ID of the order.

    Returns:
       Response: A JSON response with a success message and the HTTP status code 200 or an error message and the appropriate status code.
    """
    payload = request.get_json()
    is_valid, errors = InputValidator.validate_update_order_input(payload)

    if not is_valid:
        return Response(response=json.dumps({"data": {"error": "Invalid input", "errors": errors}}),
                        status=400, mimetype='application/json')

    try:
        updated_order = Order(id, payload.get('customer_id'), payload.get('product_ids'), 'created_time',
                              datetime.now())
        updated = order_service.update_order(updated_order)
        if not updated:
            return Response(response=json.dumps({"data": {"message": "Order not found"}}), status=404,
                            mimetype='application/json')

        else:
            return Response(
                response=json.dumps({"data": {"message": "Order updated", "order": updated_order.to_dict()}}),
                status=200, mimetype='application/json')

    except Exception:
        return Response(response=json.dumps({"data": {"error": "Internal Server Error"}}), status=500,
                        mimetype='application/json')


@orders_bp.route('/api/v1/order/<string:id>', methods=['DELETE'])
def delete_order(id: str) -> Response:
    """
    Delete an order by its ID.

    Args:
        id (str): The ID of the order.

    Returns:
        Response: A JSON response with a success message and the HTTP status code 200 or an error message and the appropriate status code.
    """
    is_valid, errors = InputValidator.validate_order_id(id)
    if not is_valid:
        return Response(response=json.dumps({"data": {"error": "Invalid input", "errors": errors}}),
                        status=400, mimetype='application/json')

    try:
        deleted = order_service.delete_order(Order(id, None, None, None, None))
        if not deleted:
            return Response(response=json.dumps({"data": {"message": "Order not found"}}), status=404,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({"data": {"message": "Order deleted", "order": deleted.to_dict()}}),
                            status=200, mimetype='application/json')

    except Exception:
        return Response(response=json.dumps({"data": {"error": "Internal Server Error"}}), status=500,
                        mimetype='application/json')
