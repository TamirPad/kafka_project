from flask import Flask
from flask_app.app.api.v1.orders_api import orders_bp
from flask_app.app.utils.kafka.kafkaAdmin import kafkaAdmin
from flask_app.app.config import Config, TestingConfig


def create_app():
    """
    Function to create a Flask application.

    Returns:
        Flask: An instance of Flask application.
    """

    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(orders_bp)

    # Create topic 'orders' if it doesn't exist
    kafka_admin = kafkaAdmin(Config.KAFKA_BOOTSTRAP_SERVERS)
    kafka_admin.init_topic(Config.KAFKA_TOPIC)

    return app
