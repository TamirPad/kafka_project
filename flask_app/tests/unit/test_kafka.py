# tests/unit/test_kafka.py

import pytest
from app.utils.kafka.kafkaAdmin import kafkaAdmin
from app.utils.kafka.kafkaClient import KafkaClient

@pytest.fixture
def kafka_admin():
    return kafkaAdmin('localhost:9092')

def test_init_topic_topic_exists(kafka_admin, caplog):
    created = kafka_admin.init_topic('orders')
    assert "Topic 'orders' already exists." in caplog.text
    assert created == False

def test_init_topic_topic_does_not_exist(kafka_admin, caplog):
    created = kafka_admin.init_topic('orders1')
    assert f"Topic 'orders1' doesn't exists." in caplog.text
    assert created == True

@pytest.fixture
def kafka_client():
    return KafkaClient(bootstrap_servers="localhost:9092")

def test_produce_message(kafka_client, caplog):
    kafka_client.produce_message(topic="orders", message="test_message") 
    assert "Message sent successfully" in caplog.text
