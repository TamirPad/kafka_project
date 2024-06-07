from flask import Flask
from app.api.v1.orders_api import orders_bp
from app.utils.kafka.kafkaAdmin import kafkaAdmin
from app.config import Config, TestingConfig



def create_app(config_class=Config):
    """
    Function to create a Flask application.

    Returns:
        Flask: An instance of Flask application.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(orders_bp)

    # Create topic 'orders' if doesn't exists
    kafkaAdmin.init_topic()
  
    return app


