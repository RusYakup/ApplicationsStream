import os
import asyncio
import logging
import aiokafka
import json
from confluent_kafka.admin import AdminClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

kafka_address = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


class KafkaConsumer:
    def __init__(self):
        logger.info("Initializing KafkaConsumer")

    async def consume_messages(self, topic: str):
        logger.info(f"Starting to consume messages from topic '{topic}'.")
        consumer = aiokafka.AIOKafkaConsumer(
            topic,
            bootstrap_servers={kafka_address},
            group_id=f"{topic}-consumer-group",
            auto_offset_reset="latest",
            enable_auto_commit=True
        )
        try:
            await consumer.start()
            async for msg in consumer:
                if msg is None:
                    continue
                if msg.value is None:
                    continue
                data = json.loads(msg.value.decode("utf-8"))
                await self.process_message(data)
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            logger.info("Stopping consumer")
            await consumer.stop()

    async def process_message(self, data):
        logger.info(f"Processing message: {data}")
        await asyncio.sleep(1)


async def main():
    logger.info("Creating Kafka admin client")
    admin_client = AdminClient({'bootstrap.servers': kafka_address})
    metadata = admin_client.list_topics(timeout=10)
    logger.debug(f"Topic metadata: {metadata.topics}")

    # Check if the topic exists
    topic_name = "new_applications"
    if topic_name in metadata.topics:
        logger.info(f"Topic '{topic_name}' exists.")
    else:
        logger.warning(f"Topic '{topic_name}' not found.")

    consumer = KafkaConsumer()
    await consumer.consume_messages("new_applications")


if __name__ == "__main__":
    logger.info("Starting consumer")
    asyncio.run(main())
