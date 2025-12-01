import asyncio
from aio_pika import connect_robust, ExchangeType, IncomingMessage, Message

from .config import RABBITMQ_URL, ORDER_EXCHANGE, ORDER_CREATED_QUEUE
from .models import Order
from .schemas import OrderCreatedEvent
from .db import connect_to_mongo, disconnect_from_mongo


async def publish_payment_request(order: Order):
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "payment.exchange", ExchangeType.TOPIC, durable=True
    )

    message = Message(
        order.json().encode(),
        content_type="application/json",
        delivery_mode=2
    )

    await exchange.publish(
        message,
        routing_key="payment.request",
    )

    print(f"📤 Sent payment.request for order {order.order_id}")
    await connection.close()


async def on_order_created_message(message: IncomingMessage):
    try:
        data = OrderCreatedEvent.model_validate_json(message.body)

        total = sum(item.price * item.quantity for item in data.items)
        items = [item.model_dump() for item in data.items]

        order_document = Order(
            order_id=data.order_id,
            user_id=data.user_id,
            items=items,
            total=total,
            status="processing"
        )

        await order_document.insert()
        print(f"🟢 Order {data.order_id} saved")

        # 🔥 THIS IS THE IMPORTANT PART
        await publish_payment_request(order_document)

        await message.ack()

    except Exception as e:
        print(f"❌ Error: {e}")
        await message.nack()


async def start_rabbitmq_consumer():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        ORDER_EXCHANGE, ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue(ORDER_CREATED_QUEUE, durable=True)
    await queue.bind(exchange, routing_key="order.created")

    print("🚀 Orders is listening...")
    await queue.consume(on_order_created_message)


async def main():
    await connect_to_mongo()
    await start_rabbitmq_consumer()
    await asyncio.Future()
