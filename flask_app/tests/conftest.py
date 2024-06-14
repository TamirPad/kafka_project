import logging
import os
import time

import pytest
import sqlalchemy
from testcontainers.kafka import KafkaContainer
from testcontainers.mysql import MySqlContainer
from testcontainers.core.container import DockerContainer
import testcontainers.core.waiting_utils as waiting_utils
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
@pytest.mark.timeout(33333)
def mariaDb() -> str:
    logging.info("** here in mariaDb fixture")
    with DockerContainer("mariadb:latest") \
            .with_exposed_ports(3306) \
            .with_env("MARIADB_ROOT_PASSWORD", "password") \
            .with_env("MARIADB_DATABASE", "db") \
            .with_env("MARIADB_USER", "user") \
            .with_env("MARIADB_PASSWORD", "pass") \
            as container:

        waiting_utils.wait_for_logs(container, "MariaDB init process done", timeout=60, interval=1)
        # Get the mapped port on the host
        host_port = container.get_exposed_port(3306)
        logging.info(f"*** MariaDB container started successfully. Port: {host_port}")

        container_info = {
                "host": "localhost",  # Assuming localhost for simplicity
                "port": host_port,
                "user": "user",
                "password": "pass",
                "database": "db"
            }

        yield container_info

@pytest.fixture(scope="session", autouse=True)
def kafka() -> KafkaContainer:
    logging.info("* here in kafka fixture")
    with KafkaContainer() as kafka:
        yield kafka

# @pytest.fixture(scope="session", autouse=True)
# @pytest.mark.timeout(33333)
# def mysql() -> MySqlContainer:
#
#     time.sleep(353425)
#     with MySqlContainer(image="mysql/mysqlserver:8.0") as mysql:
#         engine = sqlalchemy.create_engine(mysql.get_connection_url())
#
#     logging.info("** mysql container is up - now trying to create table. details: " + mysql.get_connection_url())
#     with engine.begin() as connection:
#         schema = """
#                     CREATE TABLE IF NOT EXISTS orders (
#                         id VARCHAR(255) PRIMARY KEY,
#                         customerID VARCHAR(255),
#                         product_ids VARCHAR(255),
#                         created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                         updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#                     );
#                 """
#     connection.execute(schema)
#     yield mysql

@pytest.fixture(scope="session", autouse=True)
def app(mariaDb, kafka:KafkaContainer):
    logging.info("* connection obj")

    logging.info(mariaDb)
    logging.info("db exposed port: " + mariaDb['port'])

    os.environ['KAFKA_BOOTSTRAP_SERVERS'] = kafka.get_bootstrap_server()
    os.environ['KAFKA_TOPIC'] = 'orders'
    logging.info("**** im here in app fixture.")
    # components = extract_mysql_components(mysql.get_connection_url())
    os.environ['MYSQL_HOST'] = mariaDb['host']
    os.environ['MYSQL_USER'] = mariaDb['user']
    os.environ['MYSQL_PASSWORD'] = mariaDb['password']
    os.environ['MYSQL_DB'] = mariaDb['database']
    os.environ['MYSQL_PORT'] = str(mariaDb['port'])
    from app import create_app
    app = create_app()
    yield app


@pytest.fixture(scope="session", autouse=True)
def client(app):
    return app.test_client()


# @pytest.fixture(scope="session", autouse=True)
# def app():
#     print("###SETUP TEST ENVIROMENT#####")
#     with KafkaContainer() as kafka:
#         kafkaUri = kafka.get_bootstrap_server()
#
#         # Set up MySQL container
#     with MySqlContainer('mysql:5.7.17') as mysql:
#         engine = sqlalchemy.create_engine(mysql.get_connection_url())
#
#     # Create tables in the MySQL database
#     with engine.begin() as connection:
#         schema = """
#                 CREATE TABLE IF NOT EXISTS orders (
#                     id VARCHAR(255) PRIMARY KEY,
#                     customerID VARCHAR(255),
#                     product_ids VARCHAR(255),
#                     created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#                 );
#             """
#         connection.execute(schema)
#
#     logging.info("################# mysql.get_connection ################")
#     logging.info(f"CONNECTION URI: {mysql.get_connection_url()}")
#     components = extract_mysql_components(mysql.get_connection_url())
#
#     os.environ['MYSQL_HOST'] = components['host']
#     os.environ['MYSQL_USER'] = components['user']
#     os.environ['MYSQL_PASSWORD'] = components['password']
#     os.environ['MYSQL_DB'] = components['database']
#     os.environ['MYSQL_PORT'] = str(components['port'])
#
#     os.environ['KAFKA_BOOTSTRAP_SERVERS'] = kafkaUri
#     os.environ['KAFKA_TOPIC'] = 'orders'
#
#     # Create the Flask app
#     logging.info("############### reate the Flask app ##################")
#
#     from app import create_app
#
#     app = create_app()
#
#     yield app


# @pytest.fixture()
# def client(app):
#     return app.test_client()