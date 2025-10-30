import uuid
from fastapi import FastAPI, HTTPException, status
from .schemas import OrderCreate, OrderCreatedEvent
from .rabbitmq_connector import rabbitmq_conn

app = FastAPI(
    title="E-Commerce API Gateway",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """When the app is starting"""
    try:
        await rabbitmq_conn.connect()
    except Exception as e:
        print(f"❌ Error in Starting the connection to RabbitMQ. {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """When closing the app"""
    await rabbitmq_conn.disconnect()


@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """
    Get order, creat event and publish to RabbitMQ
    """

    # Creat unique ID to order
    order_id = str(uuid.uuid4())

    # Build the event
    event_payload = OrderCreatedEvent(
        order_id=order_id,
        user_id=order_data.user_id,
        items=order_data.items,
        status="created"
    )

    try:
        # publish through the exchange
        await rabbitmq_conn.publish_order_created(event_payload)

    except ConnectionError as e:
        # If RabbitMQ is not available
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"RabbitMQ is not available, please try later. {e}"
        )

    # Return an answer to the client that his order was initiated
    return {
        "message": "Order creation successfully initiated in the queue.",
        "order_id": order_id,
        "status": "initial_creation"
    }