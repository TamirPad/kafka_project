import logging
from datetime import datetime
from typing import Tuple, Optional
import json
import uuid
from flask import Flask, render_template, jsonify, request
from orders import OrderDao, Order
from MySQL import MySQL
from config import Config
from kafka import KafkaProducer

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize database connection parameters from config
db_config = {
    'host': Config.MYSQL_HOST,
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'database': Config.MYSQL_DB,
    'port': Config.MYSQL_PORT
}

# Initialize MySQL connection
db = MySQL(**db_config)
db.connect()

# Initialize Kafka 
kafka_bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS
kafka_topic = Config.KAFKA_TOPIC

kafka_producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Initialize OrderDao
order_dao = OrderDao(db)


@app.route('/')
def index() -> str:
    orders = order_dao.get_all_orders()
    return render_template('index.html', orders=orders)

@app.route('/api/v1/order/<string:id>', methods=['GET'])
def get_order(id: str) -> Tuple[Optional[dict], int]:
    if not id:
        return jsonify({"error": "Invalid order ID format"}), 400
    order = order_dao.get_order(id)
   
    if order:
        return  {
                "id": order.id,
                "customer_id": order.customer_id,
                "product_ids": order.product_ids,
                "created_date": order.created_date.isoformat(),
                "updated_date": order.updated_date.isoformat()
                }, 200

    return jsonify({"message": "Order not found"}), 404

@app.route('/api/v1/order/', methods=['POST'])
def create_order() -> Tuple[dict, int]:
    payload = request.get_json()

    if not payload or 'customer_id' not in payload or 'product_ids' not in payload:
        return jsonify({"error": "Missing required fields: customer_id, product_ids"}), 400

    order = Order(str(uuid.uuid4()), payload.get('customer_id'), payload.get('product_ids'), datetime.now(), datetime.now())
    order_dao.create_order(order)

    order_info = {"message": "Order created", "order_id": order.id}
    kafka_producer.send(kafka_topic, value=order_info)

    return jsonify(order_info), 201

@app.route('/api/v1/order/<string:id>', methods=['PUT'])
def update_order(id: str) -> Tuple[dict, int]:
    payload = request.get_json()

    if not payload or 'customer_id' not in payload or 'product_ids' not in payload:
        return jsonify({"error": "Missing required fields: customer_id, product_ids"}), 400

    order = Order(id, payload.get('customer_id'), payload.get('product_ids'), 'unknown', datetime.now())
    order_dao.update_order(order)

    order_info = {"message": "Order updated", "order_id": id}
    kafka_producer.send(kafka_topic, value=order_info)

    return jsonify(order_info), 200

@app.route('/api/v1/order/<string:id>', methods=['DELETE'])
def delete_order(id: str) -> Tuple[dict, int]:
    if not id:
        return jsonify({"error": "Invalid order ID format"}), 400

    order_dao.delete_order(id)
    
    order_info = {"message": "Order deleted", "order_id": id}
    kafka_producer.send(kafka_topic, value=order_info)
    
    return jsonify(order_info), 200

if __name__ == '__main__':
    app.run(debug=True)
