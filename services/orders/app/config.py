import os

# RabbitMQ
RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost/")
ORDER_EXCHANGE = "order.exchange"

ORDER_CREATED_QUEUE = "order.created.queue"
PAYMENT_EXCHANGE = "payment.exchange"

# MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = "ecommerce_db"