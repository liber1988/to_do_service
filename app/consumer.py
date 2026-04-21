import json
import os
import uuid

import aio_pika
from aio_pika import ExchangeType, IncomingMessage

from app.crud.task import create_task_from_broker, delete_task_from_broker
from app.db import SessionLocal

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
REGION = os.getenv("REGION", "local")
QUEUE_NAME = f"tasks_{REGION}"


async def handle_message(message: IncomingMessage) -> None:
    async with message.process():
        payload = json.loads(message.body.decode())

        event_type = payload.get("event_type")
        source_region = payload.get("source_region")

        if source_region == REGION:
            return

        db = SessionLocal()
        try:
            if event_type == "task.created":
                create_task_from_broker(
                    db=db,
                    task_id=uuid.UUID(payload["task_id"]),
                    title=payload["title"],
                    description=payload.get("description"),
                )

            elif event_type == "task.deleted":
                delete_task_from_broker(
                    db=db,
                    task_id=uuid.UUID(payload["task_id"]),
                )
        finally:
            db.close()


async def start_consumer() -> None:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "tasks",
        ExchangeType.DIRECT,
        durable=True,
    )

    queue = await channel.declare_queue(
        QUEUE_NAME,
        durable=True,
    )

    await queue.bind(exchange, routing_key="task.created")
    await queue.bind(exchange, routing_key="task.deleted")

    await queue.consume(handle_message)