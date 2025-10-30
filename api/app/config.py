import os
RABBITMQ_URL = os.environ.get(
    "RABBITMQ_URL",
    "amqp://guest:guest@localhost/"
)

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb://localhost:27017"
)

ORDER_EXCHANGE = "order.exchange"