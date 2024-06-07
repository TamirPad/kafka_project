from flask import Flask
from app.api.v1.orders_api import orders_bp
from app.utils.sql.db import db
from app.config import Config
import logging
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

def create_app():
    """
    Function to create a Flask application.

    Returns:
        Flask: An instance of Flask application.
    """
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(orders_bp)

  
    # Create an instance of KafkaAdminClient
    admin_client = AdminClient({'bootstrap.servers':Config.KAFKA_BOOTSTRAP_SERVERS})

    # Check if the topic exists 
    try:
        topics = admin_client.list_topics().topics
    except KafkaException as e:
        logging.error(f"Failed to list topics: {e}")

    if Config.KAFKA_TOPIC in topics:
        logging.info(f"Topic '{Config.KAFKA_TOPIC}' already exists.")
    else:
        # Create the topic if it doesn't exist
        try:
            new_topic = NewTopic(Config.KAFKA_TOPIC, num_partitions=1, replication_factor=1)
            admin_client.create_topics([new_topic])
            logging.info(f"Topic '{Config.KAFKA_TOPIC}' created successfully.")
        except Exception:
            logging.error("Failed to create topic.")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
