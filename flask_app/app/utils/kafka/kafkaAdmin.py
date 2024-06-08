from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import logging

class kafkaAdmin():
    def __init__(self, kafka_bootstrap_servers: str):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
    
    def init_topic(self, topic: str):
        # Create an instance of KafkaAdminClient
        admin_client = AdminClient({'bootstrap.servers':self.kafka_bootstrap_servers})

        # Check if the topic exists 
        try:
            topics = admin_client.list_topics().topics
        except KafkaException as e:
            logging.error(f"Failed to list topics: {e}")

        if topic in topics:
            logging.info(f"Topic '{topic}' already exists.")
            return False
        else:
            # Create the topic if it doesn't exist
            logging.info(f"Topic '{topic}' doesn't exists.")
            try:
                new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
                admin_client.create_topics([new_topic])
                logging.info(f"Topic '{topic}' created successfully.")
                return True
            except Exception:
                logging.error("Failed to create topic.")