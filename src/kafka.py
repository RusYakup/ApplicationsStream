import logging
import aiokafka
import json
from src.config import Settings

log = logging.getLogger(__name__)


class KafkaPublisher:
    def __init__(self, config: Settings):
        self.config = config

    async def publish_message(self, topic: str, message: dict):

        producer = aiokafka.AIOKafkaProducer(
            client_id="producer",
            bootstrap_servers=self.config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        try:
            log.debug(f"Starting producer for topic {topic}")
            await producer.start()
            log.debug(f"Publishing message to topic {topic}: {message}")
            await producer.send_and_wait(topic, message)
            log.debug(f"Message published to topic {topic}: {message}")
        except Exception as e:
            log.error(f"Failed to publish message to topic {topic}: {e}")
        finally:
            await producer.stop()
            log.debug(f"Stopped producer for topic {topic}")


kafka_publisher = KafkaPublisher(Settings())