import json
import os

import aio_pika
from aio_pika import ExchangeType, Message, RobustChannel, RobustConnection


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = "tasks"


async def connect_broker() -> tuple[RobustConnection, RobustChannel]:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    await channel.declare_exchange(
        EXCHANGE_NAME,
        ExchangeType.TOPIC,
        durable=True,
    )

    return connection, channel


async def publish_event(
    channel: RobustChannel,
    routing_key: str,
    payload: dict,
) -> None:
    exchange = await channel.get_exchange(EXCHANGE_NAME)

    message = Message(
        body=json.dumps(payload).encode("utf-8"),
        content_type="application/json",
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )

    await exchange.publish(message, routing_key=routing_key)