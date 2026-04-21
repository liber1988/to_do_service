import json
import os

import aio_pika
from aio_pika import ExchangeType, Message
from fastapi import FastAPI

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")


async def connect_rabbitmq(app: FastAPI) -> None:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    await channel.declare_exchange(
        "tasks",
        ExchangeType.DIRECT,
        durable=True,
    )

    app.state.rabbit_connection = connection
    app.state.rabbit_channel = channel


async def publish_event(channel, routing_key: str, payload: dict) -> None:
    exchange = await channel.get_exchange("tasks")
    await exchange.publish(
        Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=routing_key,
    )