import logging
from flask import Flask, render_template, jsonify, request
from MySQL import MySQL
import uuid
from datetime import datetime
import config
from config import Config
from typing import Tuple, Optional
from kafka import KafkaProducer
import json


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize database connection parameters from config
db_config = {
    'host': Config.MYSQL_HOST,
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'database': Config.MYSQL_DB,
    'port': Config.MYSQL_PORT
}

# Initialize Kafka 
kafka_bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS
kafka_topic = Config.KAFKA_TOPIC

kafka_producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def get_db_connection() -> MySQL:
    """
    Create and return a new MySQL database connection.

    :return: MySQL database connection
    """
    db = MySQL(**db_config)
    db.connect()
    return db

@app.route('/')
def index() -> str:
    """
    Render the index page with a list of orders from the database.

    :return: Rendered HTML template with orders data
    """
    db = get_db_connection()
    query = "SELECT * FROM orders"
    result = db.execute_query(query)
    orders = [
        {"id": row['id'], "customer_id": row['customerID'], "product_ids": row['product_ids'],
         "created_date": row['created_date'], "updated_date": row['updated_date']} for row in result]
    db.disconnect()
    return render_template('index.html', orders=orders)

@app.route('/api/v1/order/<string:id>', methods=['GET'])
def get_order(id: str) -> Tuple[Optional[dict], int]:
    """
    Get a specific order by its ID.

    :param id: The ID of the order to retrieve
    :return: JSON response with order details and HTTP status code
    """
    db = get_db_connection()
    query = "SELECT * FROM orders WHERE id = %s"
    result = db.execute_query(query, params=(id,))
    db.disconnect()

    if result:
        order = {
            "id": result[0]['id'],
            "customer_id": result[0]['customerID'],
            "product_ids": result[0]['product_ids'],
            "created_date": result[0]['created_date'],
            "updated_date": result[0]['updated_date']
        }
        return jsonify(order), 200
    return jsonify({"message": "Order not found"}), 404

@app.route('/api/v1/order/', methods=['POST'])
def create_order() -> Tuple[dict, int]:
    """
    Create a new order.

    :return: JSON response with the created order ID and HTTP status code
    """
    data = request.get_json()
    logging.debug(f"Received data: {data}")

    if not data or 'customer_id' not in data or 'product_ids' not in data:
        return jsonify({"message": "Invalid request"}), 400

    order_id = str(uuid.uuid4())
    customer_id = str(data['customer_id'])
    product_ids = str(data['product_ids'])
    created_date = datetime.now()
    updated_date = created_date

    db = get_db_connection()
    query = """
            INSERT INTO orders (id, customerID, product_ids, created_date, updated_date) 
            VALUES (%s, %s, %s, %s, %s)
        """
    params = (order_id, customer_id, product_ids, created_date, updated_date)
    db.execute_query(query, params=params)
    db.disconnect()

    order_info = {"message": "Order created", "order_id": order_id}
    kafka_producer.send(kafka_topic, value=order_info)

    return jsonify(order_info), 201


@app.route('/api/v1/order/<string:id>', methods=['PUT'])
def update_order(id: str) -> Tuple[dict, int]:
    """
    Update an existing order by its ID.

    :param id: The ID of the order to update
    :return: JSON response with a success message and HTTP status code
    """
    data = request.get_json()

    if not data or 'customer_id' not in data or 'product_ids' not in data:
        return jsonify({"message": "Invalid request"}), 400

    db = get_db_connection()
    query = "UPDATE orders SET customerID = %s, product_ids = %s, updated_date = %s WHERE id = %s"
    params = (data['customer_id'], data['product_ids'], datetime.now(), id)
    db.execute_query(query, params=params)
    db.disconnect()

    order_info = {"message": "Order updated", "order_id": id}
    kafka_producer.send(kafka_topic, value=order_info)

    return jsonify(order_info), 200

@app.route('/api/v1/order/<string:id>', methods=['DELETE'])
def delete_order(id: str) -> Tuple[dict, int]:
    """
    Delete an order by its ID.

    :param id: The ID of the order to delete
    :return: JSON response with a success message and HTTP status code
    """
    db = get_db_connection()
    query = "DELETE FROM orders WHERE id = %s"
    db.execute_query(query, params=(id,))
    db.disconnect()

    order_info = {"message": "Order deleted", "order_id": id}
    kafka_producer.send(kafka_topic, value=order_info)

    return jsonify(order_info), 200

if __name__ == '__main__':
    app.run(debug=True)
