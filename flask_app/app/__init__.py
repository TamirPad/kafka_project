from flask import Flask
from app.api.v1.orders_api import orders_bp
from app.utils.kafka.kafkaAdmin import kafkaAdmin
from app.config import Config, TestingConfig



def create_app():
    """
    Function to create a Flask application.

    Returns:
        Flask: An instance of Flask application.
    """

    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(orders_bp)

    # Create topic 'orders' if doesn't exists
    kafka_admin = kafkaAdmin(Config.KAFKA_BOOTSTRAP_SERVERS)
    kafka_admin.init_topic(Config.KAFKA_TOPIC)
  
    return app


