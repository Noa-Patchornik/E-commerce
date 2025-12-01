# services/payment/app/schemas.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float


class OrderCreatedEvent(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    status: str


class PaymentEvent(BaseModel):
    order_id: str
    transaction_id: str
    amount: float
    status: str = Field(default="succeeded")  # succeeded / failed
    timestamp: datetime = Field(default_factory=datetime.utcnow)
