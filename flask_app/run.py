from flask import Flask
from app.api.v1.orders_api import orders_bp
from app.utils.sql.db import db
from app.utils.kafka.kafkaAdmin import kafkaAdmin
from app.config import Config
import logging


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
    kafkaAdmin.init_topic()
  
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
