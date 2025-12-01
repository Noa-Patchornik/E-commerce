# services/payment/app/main.py
import asyncio
from aio_pika import connect_robust, ExchangeType, IncomingMessage, Message

from .config import settings
from .db import connect_to_mongo, disconnect_from_mongo
from .schemas import OrderCreatedEvent, PaymentEvent
from .utils import simulate_payment


async def on_order_created_message(message: IncomingMessage):
    try:
        print("📥 RAW:", message.body)

        import json
        payload = json.loads(message.body.decode())   # ← הפתרון
        print("🔍 Decoded JSON:", payload)

        data = OrderCreatedEvent(**payload)
        print("✅ Parsed event:", data)

        total = sum(item.price * item.quantity for item in data.items)

        transaction = await simulate_payment(
            data.order_id,
            data.user_id,
            total
        )

        await publish_payment_event(transaction)
        await message.ack()

    except Exception as e:
        print(f"❌ Error processing message: {e}")
        await message.nack(requeue=False)



async def publish_payment_event(transaction):
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        settings.PAYMENT_EXCHANGE, ExchangeType.TOPIC, durable=True
    )

    event = PaymentEvent(
        order_id=transaction.order_id,
        transaction_id=transaction.transaction_id,
        amount=transaction.amount,
        status=transaction.status,
    )

    routing_key = (
        settings.PAYMENT_SUCCEEDED_ROUTING_KEY
        if transaction.status == "succeeded"
        else settings.PAYMENT_FAILED_ROUTING_KEY
    )

    await exchange.publish(
        Message(event.model_dump_json().encode()),
        routing_key=routing_key,
    )

    print(f"📤 Published event '{routing_key}' for order {transaction.order_id}")
    await connection.close()


async def start_consumer():
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)

    # Payment should listen to PAYMENT_EXCHANGE, not ORDER_EXCHANGE!
    exchange = await channel.declare_exchange(
        settings.PAYMENT_EXCHANGE, ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue(
        settings.PAYMENT_REQUEST_QUEUE,
        durable=True
    )

    await queue.bind(exchange, "payment.request")
    await queue.consume(on_order_created_message)

    print("🔥 PAYMENT is LISTENING to:", settings.PAYMENT_REQUEST_QUEUE)
    return connection



async def app_start():
    await connect_to_mongo()
    connection = await start_consumer()

    # keep service running
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await connection.close()
        await disconnect_from_mongo()


def main():
    asyncio.run(app_start())


if __name__ == "__main__":
    main()
