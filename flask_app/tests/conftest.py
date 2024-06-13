import pytest
import logging
import sqlalchemy
import json
from testcontainers.mysql import MySqlContainer
from testcontainers.kafka import KafkaContainer
import os
from app.config import Config
import time


# Set up logging
logging.basicConfig(level=logging.DEBUG)




from urllib.parse import urlparse

def extract_mysql_components(connection_string):
    # Parse the connection string
    result = urlparse(connection_string)
    
    # Extract components
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    database = result.path.lstrip('/')  # Remove leading slash from the path

    return {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'database': database
    }



@pytest.fixture(scope="session", autouse=True)
def app():
    print("###SETUP TEST ENVIROMENT#####")
  



    # Set up MySQL container
    with MySqlContainer('mysql:5.7.17') as mysql:
        engine = sqlalchemy.create_engine(mysql.get_connection_url())

        # Create tables in the MySQL database
        with engine.begin() as connection:
            schema = """
                CREATE TABLE IF NOT EXISTS orders (
                    id VARCHAR(255) PRIMARY KEY, 
                    customerID VARCHAR(255),
                    product_ids VARCHAR(255),
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
            """
            connection.execute(schema)

        logging.info("################# mysql.get_connection ################")
        logging.info(f"CONNECTION URI: {mysql.get_connection_url()}")
        components = extract_mysql_components(mysql.get_connection_url())



        os.environ['MYSQL_HOST'] = components['host']
        os.environ['MYSQL_USER'] = components['user']
        os.environ['MYSQL_PASSWORD'] = components['password']
        os.environ['MYSQL_DB'] = components['database']
        os.environ['MYSQL_PORT'] = str(components['port'])

        os.environ['KAFKA_BOOTSTRAP_SERVERS'] = 'localhost:9092'
        os.environ['KAFKA_TOPIC'] = 'orders'


        
        # Create the Flask app
        logging.info("############### reate the Flask app ##################")

        from app import create_app

        app = create_app()

        yield app

@pytest.fixture()
def client(app):
    return app.test_client()

