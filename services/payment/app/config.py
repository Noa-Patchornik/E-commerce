# services/payment/app/config.py
import os
from pydantic import BaseModel


class Settings(BaseModel):
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://admin:admin@rabbitmq/")
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ecommerce")

    ORDER_EXCHANGE: str = os.getenv("ORDER_EXCHANGE", "order.exchange")
    ORDER_CREATED_QUEUE: str = os.getenv("ORDER_CREATED_QUEUE", "payment.order.created.queue")

    PAYMENT_EXCHANGE = "payment.exchange"
    PAYMENT_REQUEST_QUEUE = "payment.request.queue"
    PAYMENT_SUCCEEDED_ROUTING_KEY: str = "payment.succeeded"
    PAYMENT_FAILED_ROUTING_KEY: str = "payment.failed"


settings = Settings()
