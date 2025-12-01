# E-Commerce Microservices -- System Status & Documentation

## 📁 Project Structure

    E-commerce/
    ├─ api/
    │  ├─ app/
    │  │  ├─ main.py
    │  │  ├─ rabbitmq_connector.py
    │  │  ├─ schemas.py
    │  │  ├─ config.py
    │  ├─ Dockerfile
    │  ├─ requirements.txt
    │
    ├─ services/
    │  ├─ orders/
    │  │  ├─ app/
    │  │  │  ├─ main.py
    │  │  │  ├─ models.py
    │  │  │  ├─ schemas.py
    │  │  │  ├─ config.py
    │  │  │  ├─ db.py
    │  ├─ payment/
    │  │  ├─ app/
    │  │  │  ├─ main.py
    │  │  │  ├─ models.py
    │  │  │  ├─ schemas.py
    │  │  │  ├─ config.py
    │  │  │  ├─ db.py
    │  │  │  ├─ utils.py
    │  ├─ Dockerfile
    │  ├─ requirements.txt
    │
    ├─ infra/
    │  ├─ rabbitmq_definitions.json
    │
    ├─ docker-compose.yml

------------------------------------------------------------------------

## ✅ What Works Now

### API Gateway

-   Receives orders (`POST /orders`)
-   Creates event `order.created`
-   Publishes event to RabbitMQ exchange `order.exchange`
-   Fully functional and tested

### Orders Service

-   Listens to `order.created`
-   Computes total price
-   Saves order into MongoDB
-   Works 100% and logs confirmed processing

### Infrastructure

-   RabbitMQ running and healthy
-   MongoDB running
-   Prometheus + Grafana running
-   RabbitMQ definitions loaded successfully

------------------------------------------------------------------------

## ⚠️ Currently Under Debugging --- Payment Service

### Behavior:

-   Payment service **starts successfully**, connects to Mongo, waits
    for messages
-   Does **NOT receive** `order.created` events

### Root Cause:

Mismatch in queue name:

  Service   Queue
  --------- -------------------------------
  Orders    `payment.order.created.queue`
  Payment   `order.created.queue`

This prevents consumption of messages.

### Fix Applied:

Payment config updated:

    ORDER_CREATED_QUEUE="payment.order.created.queue"

### Still pending:

Even after fix, payment service does not consume messages.\
We need to verify: - Exchange & queue exist in RabbitMQ UI - Queue is
bound correctly - Events actually arrive to RabbitMQ

------------------------------------------------------------------------

## 🧪 How to Test the System

### Test order creation

PowerShell:

``` powershell
Invoke-RestMethod -Uri "http://localhost:8000/orders" `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"user_id": "u-999", "items": [{"product_id": "p-777", "quantity": 1, "price": 120.5}]}'
```

Expected:

    order_id + initial_creation

### Check Orders Service Logs:

    docker-compose logs orders

Expected:

    🎉 Order <uuid> saved to DB

### Check Payment Logs:

    docker-compose logs payment

Expected (NOT YET WORKING):

    Payment Service Consumer started...

------------------------------------------------------------------------

## 🛠️ Next Steps

### Step 1 --- Verify queue existence in RabbitMQ

1.  Open: http://localhost:15672
2.  Go to **Queues**
3.  Find: `payment.order.created.queue`
4.  Check message counters (Ready / Unacked)

### Step 2 --- Reproduce binding manually

Ensure Payment service executes:

    queue.bind("order.exchange", "order.created")

### Step 3 --- Fix payment not receiving messages

We will inspect: - Binding confirmation logs - Exchange/queue creation
logs - Routing key mapping

### Step 4 --- Add next microservices:

-   Inventory service
-   Notification service
-   Payment → Order update chain

------------------------------------------------------------------------

## 📌 Summary

You have: ✔ Fully working API\
✔ Fully working Orders Service\
✔ Working infra (RabbitMQ, Mongo, Grafana, Prometheus)\
⚠ Payment service runs but does not receive events

Next, we debug RabbitMQ routing to Payment.
