import json
from aio_pika import connect_robust, ExchangeType, Message, RobustConnection, RobustChannel
from .config import RABBITMQ_URL, ORDER_EXCHANGE
from .schemas import OrderCreatedEvent


class RabbitMQConnector:
    """
    Class to connect and publish messages to RabbitMQ
    """

    def __init__(self):
        self.connection: RobustConnection = None
        self.channel: RobustChannel = None
        self.order_exchange = None

    async def connect(self):
        """Conner and define the Exchanges"""
        print(f"Connecting to RabbitMQ at {RABBITMQ_URL}...")
        self.connection = await connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()


        self.order_exchange = await self.channel.declare_exchange(
            ORDER_EXCHANGE,
            ExchangeType.TOPIC,
            durable=True
        )
        print(f"✅ RabbitMQ Exchange '{ORDER_EXCHANGE}' Ready to use")

    async def disconnect(self):
        """Close the connection to RabbitMQ"""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def publish_order_created(self, event_data: OrderCreatedEvent):
        """publish to order_exchange"""
        if not self.order_exchange:
            raise ConnectionError("RabbitMQ Exchange not available.")

        message_body = event_data.model_dump_json().encode()

        message = Message(
            message_body,
            content_type='application/json',
            delivery_mode=2
        )

        await self.order_exchange.publish(
            message,
            routing_key="order.created"
        )
        print(f"🎉 published an event for order: {event_data.order_id}")


rabbitmq_conn = RabbitMQConnector()