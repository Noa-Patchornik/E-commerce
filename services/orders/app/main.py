import asyncio
import json
from aio_pika import connect_robust, ExchangeType, IncomingMessage, Message

from .config import RABBITMQ_URL, ORDER_EXCHANGE, ORDER_CREATED_QUEUE
from .models import Order
from .schemas import OrderCreatedEvent
from .db import connect_to_mongo, disconnect_from_mongo



async def on_order_created_message(message: IncomingMessage):
    """
    Function to deal with an order when a message is coming
    """
    try:
        data = OrderCreatedEvent.model_validate_json(message.body)

        # calculate the total amount of the order by using the price in each item
        total = sum(item.price * item.quantity for item in data.items)

        items_for_db = [item.model_dump() for item in data.items]

        # create an object for the DB
        order_document = Order(
            order_id=data.order_id,
            user_id=data.user_id,
            items=items_for_db,
            total=total,
            status="processing"
        )

        # save the new order in the DB
        await order_document.insert()
        print(f"🎉 Order {data.order_id} saved to DB with total: {total}")

        # 5. TODO: פרסום אירוע הבא: order.validated או payment.request (נבנה בהמשך)
        # זה יבוא בשלב הבא!

        # Ack to Rabbit so the message would get out of the queue
        await message.ack()

    except Exception as e:
        print(f"❌ Error processing message {message.routing_key} for order {data.order_id}: {e}")
        await message.nack()


# --- Consumer Setup ---

async def start_rabbitmq_consumer():
    """create the consumer that will consume from the queue"""
    connection = await connect_robust(RABBITMQ_URL)

    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        ORDER_EXCHANGE, ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue(ORDER_CREATED_QUEUE, durable=True)
    await queue.bind(exchange, routing_key="order.created")
    print(f"✅ Bound queue '{ORDER_CREATED_QUEUE}' to exchange '{ORDER_EXCHANGE}' with key 'order.created'")

    await queue.consume(on_order_created_message, no_ack=False)
    print("🚀 Order Service Consumer started...")


async def main():

    await connect_to_mongo()
    await start_rabbitmq_consumer()

    await asyncio.Future()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n👋 Order Service shutting down...")
    finally:
        loop.run_until_complete(disconnect_from_mongo())
        loop.close()