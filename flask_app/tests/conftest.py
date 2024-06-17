import logging
import os
import time

import pytest
from testcontainers.kafka import KafkaContainer
from testcontainers.core.container import DockerContainer
import testcontainers.core.waiting_utils as waiting_utils
from confluent_kafka import Consumer, KafkaError

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="session", autouse=True)
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


@pytest.fixture(scope='module')
def kafka_consumer(kafka: KafkaContainer):
    consumer = Consumer({
        'bootstrap.servers': kafka.get_bootstrap_server(),
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['orders'])

    yield consumer
    consumer.close()


@pytest.fixture(scope="session", autouse=True)
def app(mariaDb, kafka: KafkaContainer):
    logging.info("* connection obj")

    logging.info(mariaDb)
    logging.info("db exposed port: " + mariaDb['port'])

    os.environ['KAFKA_BOOTSTRAP_SERVERS'] = kafka.get_bootstrap_server()
    os.environ['KAFKA_TOPIC'] = 'orders'

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

class KafkaTestKey():
    def __init__(self):
        self.messages = List()
