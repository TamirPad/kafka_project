import logging
import threading
from typing import Dict, List, Any
from confluent_kafka import KafkaError, Consumer, Message
from flask_app.app.utils.kafka.kafka_messages.serializers.proto_order_serializer import ProtoOrderSerializer
from flask_app.app.utils.kafka.kafka_messages.serializers.generated_protobuf.order_event_pb2 import Order, OperationType, OrderMessage


class KafkaMessageHolder:
    def __init__(self, kafka_consumer: Consumer) -> None:
        self.consumer: Consumer = kafka_consumer
        self.messages: Dict[str, List[Any]] = {}
        self.lock: threading.Lock = threading.Lock()
        self._running: bool = True

    def handle_error(self, error: KafkaError) -> None:
        if error.code() == KafkaError._PARTITION_EOF:
            logging.info(f"End of partition reached {error.topic()}/{error.partition()}")
        else:
            logging.error(f"Kafka error: {error}")
            self._running = False

    def process_message(self, msg: Message) -> None:
        order_message = ProtoOrderSerializer.deserialize_order(msg.value())
        logging.info(f'[KafkaMessageHolder] Received message: {order_message}')

        with self.lock:
            if order_message.order.id not in self.messages:
                self.messages[order_message.order.id] = []
            self.messages[order_message.order.id].append(order_message)

    def poll_message(self) -> None:
        msg: Message = self.consumer.poll(1.0)
        if msg is None:
            return
        if msg.error():
            self.handle_error(msg.error())
        else:
            self.process_message(msg)

    def consume_messages(self) -> None:
        while self._running:
            self.poll_message()

    def start_consuming(self) -> None:
        self.consumer_thread = threading.Thread(target=self.consume_messages)
        self.consumer_thread.start()

    def stop_consuming(self) -> None:
        self._running = False
        self.consumer_thread.join()

    def get_messages_by_order_id(self, order_id: str) -> List[Any]:
        with self.lock:
            return self.messages.get(order_id, [])
